from streamlit import error, user

from Schemas.schemas import User_Register_Input, LoginInputSchema, Store_interactions
from Database.models import Users, Researchers, Admins, RecommendorAlgorithms, Content, Interactions
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC,generate_interactionid
from Database.db import get_db
import datetime
from sqlalchemy import select, func

UserRouter = APIRouter(prefix='/UserRoutes')

@UserRouter.post("/register")
async def Register(User: User_Register_Input, db: Session = Depends(get_db)):

    DupeUsernameCheck = db.execute(
        select(Users).where(Users.USERNAME == User.Username)
    ).scalar_one_or_none()
    
    if DupeUsernameCheck is not None:
        raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
    else:
        GenerateduserID = generate_userid()
        Hashed_Password = hash_password(User.Password)

        Gender_Map = {"Male": 1, "Female": 2}

        new_user = Users(
            USER_ID = GenerateduserID,
            FIRST_NAME=User.Firstname,
            LAST_NAME=User.Lastname,
            USERNAME=User.Username,
            PASSWORD=Hashed_Password,
            GENDER=Gender_Map[User.Gender],
            AGE=User.Age,
            PREFERRED_CATEGORIES=User.PreferredCategories,
            PREFERRED_SUB_CATEGORIES=User.PreferredSubCategories
            )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "message": "Registration successful",
            "username": new_user.USERNAME
        }



@UserRouter.get("/recommendations")
async def recommendations(request: Request, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)

    if rbac_result["role"] != "Users":
        raise UserNotAuthorized()

    user_category_preferences = db.execute(
        select(Users).where(Users.USER_ID == rbac_result["user_id"])
    ).scalar_one_or_none()

    preferred_categories = user_category_preferences.PREFERRED_CATEGORIES


    #fetch current recommder from RecommendorAlgorithms.CURRENTLY_ACTIVE and get recs form that
    #find th foldr of the uploaded file and run the code

    FindAlgorithm = db.execute(
        select(RecommendorAlgorithms).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == "Yes")
    ).scalar_one_or_none()

    import importlib

    module = importlib.import_module(f"RECSYS_V2_RECOMMENDER.{FindAlgorithm.ALGORITHM_NAME}")
    load_data = module.load_data #need to change to abc class fit
    CategoryMeanRecommender = module.CategoryMeanRecommender #need to change to abc class recommend
        
    df = load_data(db)
    model = CategoryMeanRecommender()
    model.fit(df)
    final_recs = model.recommend(preferred_categories) #returned are ordered recommded ids need to fetch from db

    recommendations = db.execute(
        select(Content).where(Content.ITEM_ID.in_(final_recs))
    ).scalars().all()

    # Rank this user's interactions per item, newest first
    ranked_interactions = (
        select(
            Interactions.ITEM_ID,
            Interactions.INTERACTION_TYPE,
            Interactions.TIMESTAMP,
            func.row_number().over(
                partition_by=Interactions.ITEM_ID,
                order_by=Interactions.TIMESTAMP.desc()
            ).label("rn")
        )
        .where(
            Interactions.USER_ID == rbac_result["user_id"],
            Interactions.ITEM_ID.in_(final_recs)
        )
        .subquery()
    )

    latest_interaction = (
        select(ranked_interactions)
        .where(ranked_interactions.c.rn == 1)
        .subquery()
    )

    results = db.execute(
        select(Content, latest_interaction.c.INTERACTION_TYPE, latest_interaction.c.TIMESTAMP)
        .outerjoin(latest_interaction, latest_interaction.c.ITEM_ID == Content.ITEM_ID)
        .where(Content.ITEM_ID.in_(final_recs))
    ).all()

    recommendations = [
        {
            "ITEM_ID": content.ITEM_ID,
            "DATASET_NAME": content.DATASET_NAME,
            "CATEGORY": content.CATEGORY,
            "SUB_CATEGORY": content.SUB_CATEGORY,
            "TITLE": content.TITLE,
            "ABSTRACT": content.ABSTRACT,
            "TIMESTAMP": content.TIMESTAMP,
            "ARTICLE_TYPE": content.ARTICLE_TYPE,
            "CURRENT_INTERACTION_TYPE": interaction_type,  # None if user never interacted
        }
        for content, interaction_type, interaction_ts in results
    ]
    return recommendations

@UserRouter.post("/interactions") #take in item id intercation type
async def interactions(request: Request, Interaction_input: Store_interactions, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)

    if rbac_result["role"] != "Users":
        raise UserNotAuthorized()


    #check item for existing interactions
    #user can either like, dislike, report or dislike and report
    #we dont remove interactions based on if a user likes then dislikes later, we keep all interactions even if the same item for complex model traning later on, to show the current interaction we get the newest interaction record for that item id


    existing_interaction = db.execute(
        select(Interactions).where(Interactions.ITEM_ID == Interaction_input.INTERACTION_TYPE)
    ).scalar_one_or_none()#

    GeneratedInteractionId = generate_interactionid()

    CurrentActiveAlgorithm = db.execute(
        select(RecommendorAlgorithms.ALGORITHM_NAME).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == True)
    ).scalar_one_or_none()


    
    new_interaction = Interactions(
        DATASET_NAME = "RECSYS_V2",
        INTERACTION_ID = GeneratedInteractionId,
        USER_ID = rbac_result["user_id"],
        ITEM_ID = Interaction_input.ITEM_ID,
        TIMESTAMP = datetime.datetime.now(),
        INTERACTION_TYPE = Interaction_input.INTERACTION_TYPE,
        READ_TIME = None,
        SCROLL_PERCENTAGE = None,
        ALGORITHM_USED = CurrentActiveAlgorithm
        )

        
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction








#users need to choose category preference as soon as he registers
#for now just manually select preferences througa route or mnual db edit

#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html