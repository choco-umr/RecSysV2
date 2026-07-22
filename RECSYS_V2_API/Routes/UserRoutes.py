from streamlit import error, user

from Schemas.schemas import User_Register_Input, LoginInputSchema
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies
from Database.db import get_db

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

        new_user = Users(
            USER_ID = GenerateduserID,
            USER_TYPE = "User",
            FIRST_NAME=User.Firstname,
            LAST_NAME=User.Lastname,
            USERNAME=User.Username,
            PASSWORD=Hashed_Password,
            GENDER=User.Gender,
            AGE=User.Age
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html