from Schemas.schemas import User_Register_Input, LoginInputSchema
from Database.models import Users
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password
from Database.db import get_db

UserRouter = APIRouter(prefix='/UserRoutes')

@UserRouter.post("/register")
async def Register(User: User_Register_Input, db: Session = Depends(get_db)):
 
    GenerateduserID = generate_userid()
    Hashed_Password = hash_password(User.Password)

    new_user = Users(
        USER_ID = GenerateduserID,
        USER_TYPE = "User", #excluded from schema, User can only be Normal user not researcher
        FIRST_NAME=User.Firstname,
        LAST_NAME=User.Lastname,
        USERNAME=User.Username,
        PASSWORD=Hashed_Password,
        GENDER=User.Gender,
        AGE=User.Age
        )
    
    #unique user id chec
    #unique username check

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@UserRouter.post("/login")
async def Login(LoginInput: LoginInputSchema, db: Session = Depends(get_db)):

    UsernameExtract = select(Users).where(Users.USERNAME == LoginInput.Username)

    user = db.scalars(UsernameExtract).first() #if empty means username doesnt exist

    if verify_password(user.PASSWORD, LoginInput.Password):
        print("password correct")
        return {"message": "Success"}
    else:
        raise HTTPException(status_code=401, detail="wrong password err unauth ")
    #jwt code





#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html