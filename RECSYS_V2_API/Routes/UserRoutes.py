from streamlit import error, user

from Schemas.schemas import User_Register_Input, LoginInputSchema
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Database.db import get_db
from RECSYS_V2_RECOMMENDER import Base, RContentBasedFiltering
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
        select(Users).where(Users.USER_ID == user_id)
    ).scalar_one_or_none()

    preferred_categories = user_category_preferences.PREFERRED_CATEGORIES


    #fetch current recommder from RecommendorAlgorithms.CURRENTLY_ACTIVE and get recs form that
    #find th foldr of the uploaded file and run the code

    FindAlgorithm = db.execute(
        select(RecommendorAlgorithms).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == "Yes")
    ).scalar_one_or_none()

    #locate the file in /recommders folder wiht the RecommendorAlgorithms.filename and run that code
    folder = f"/RECSYS_V2_RECOMMENDER/{FindAlgorithm.CURRENTLY_ACTIVE}"
    


    df = load_data(db)
    model = CategoryMeanRecommender()
    model.fit(df)
    final_recs = model.recommend(preferred_categories) #returned are ordered recommded ids need to fetch from db


    recommendations = db.execute(
        select(Content).where(Content.ITEM_ID.in_(final_recs))
    ).scalars().all()

    return recommendations



#users need to choose category preference as soon as he registers
#for now just manually select preferences througa route or mnual db edit

#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html