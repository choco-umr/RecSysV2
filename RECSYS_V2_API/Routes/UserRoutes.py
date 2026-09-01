import datetime

from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from Schemas.schemas import user_register_input, login_input_schema, store_interactions

from Database.models import Users, Researchers, Admins, RecommendorAlgorithms, Content, Interactions
from Database.db import get_db

from Security.security import hash_password, generate_user_id, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC, generate_interaction_id
from Security.exceptions import user_not_authorized

user_router = APIRouter(prefix='/user_routes')

@user_router.post("/register")
async def register(User: user_register_input, db: Session = Depends(get_db)):

    dupe_username_check = db.execute(
        select(Users).where(Users.USERNAME == User.username)
    ).scalar_one_or_none()

    if dupe_username_check is not None:
        raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
    else:
        generated_user_id = generate_user_id()
        hashed_password = hash_password(User.password)

        gender_map = {"Male": 1, "Female": 2}

        new_user = Users(
            USER_ID = generated_user_id,
            FIRST_NAME=User.firstname,
            LAST_NAME=User.lastname,
            USERNAME=User.username,
            PASSWORD=hashed_password,
            GENDER=gender_map[User.gender],
            AGE=User.age,
            PREFERRED_CATEGORIES=User.preferred_categories,
            PREFERRED_SUB_CATEGORIES=User.preferred_sub_categories
            )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "message": "Registration successful",
            "username": new_user.USERNAME
        }



@user_router.get("/recommendations")
async def recommendations(request: Request, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)

    if rbac_result["role"] != "Users":
        raise user_not_authorized()

    user_category_preferences = db.execute(
        select(Users).where(Users.USER_ID == rbac_result["user_id"])
    ).scalar_one_or_none()

    preferred_categories = user_category_preferences.PREFERRED_CATEGORIES


    #fetch current recommder from RecommendorAlgorithms.CURRENTLY_ACTIVE and get recs form that
    #find th foldr of the uploaded file and run the code

    find_algorithm = db.execute(
        select(RecommendorAlgorithms).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == "Yes")
    ).scalar_one_or_none()

    import importlib

    module = importlib.import_module(f"RECSYS_V2_RECOMMENDER.{find_algorithm.ALGORITHM_NAME}")
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



@user_router.post("/interactions") #take in item id intercation type
async def interactions(request: Request, interaction_input: store_interactions, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)

    if rbac_result["role"] != "Users":
        raise user_not_authorized()

    existing_interaction = db.execute(
        select(Interactions).where(Interactions.ITEM_ID == interaction_input.item_id)
    ).scalar_one_or_none()#

    generated_interaction_id = generate_interaction_id()

    current_active_algorithm = db.execute(
        select(RecommendorAlgorithms.ALGORITHM_NAME).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == True)
    ).scalar_one_or_none()


    new_interaction = Interactions(
        DATASET_NAME = "RECSYS_V2",
        INTERACTION_ID = generated_interaction_id,
        USER_ID = rbac_result["user_id"],
        ITEM_ID = interaction_input.item_id,
        TIMESTAMP = datetime.datetime.now(),
        INTERACTION_TYPE = interaction_input.interaction_type,
        READ_TIME = None,
        SCROLL_PERCENTAGE = None,
        ALGORITHM_USED = current_active_algorithm
        )
        
    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)

    return new_interaction


# NOTES
"""
- recommendations: fetch the currently active algorithm from RecommendorAlgorithms.CURRENTLY_ACTIVE and run recs from that; also needs to locate the folder of the uploaded file and run its code
- recommendations: load_data / CategoryMeanRecommender need to be swapped for an ABC base class (fit/recommend interface) instead of ad-hoc module attributes
- recommendations: final_recs comes back as ordered recommended ids that still need to be fetched from the db
- interactions endpoint: takes item id + interaction type
- interactions: user can like, dislike, report, or dislike+report
- interactions: we don't remove/overwrite past interactions when a user changes their mind (e.g. likes then later dislikes) — all interactions are kept for future model training; "current" interaction is derived by taking the newest record per item id
- registration: users need to choose category preferences right after registering; for now preferences are set manually via a route or direct db edit
- TODO: clean up all HTTPExceptions (standardize error handling)
- Reference: OWASP JWT security cheat sheet — https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
"""