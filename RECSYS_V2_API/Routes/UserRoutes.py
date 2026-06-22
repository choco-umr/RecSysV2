from Schemas.schemas import User_Register_Input, LoginInputSchema
from Database.models import Users
from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies
from Database.db import get_db
UserRouter = APIRouter(prefix='/UserRoutes')

@UserRouter.post("/register")
async def Register(User: User_Register_Input, db: Session = Depends(get_db)):
 
    GenerateduserID = generate_userid()
    Hashed_Password = hash_password(User.Password)

    new_user = Users(
        USER_ID = GenerateduserID,
        USER_TYPE = "User", #excluded from schema, User can only be Normal user not researcher ?
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

    user = db.scalars(UsernameExtract).first() #if empty means need to catch if empty or err, username doesnt exist

    #check if already logged in

    if verify_password(user.PASSWORD, LoginInput.Password):
        print("password correct")
        access_token = create_jwt_token(str(user.USER_ID), str(user.USER_TYPE))
        print("acess token created", access_token)
        response = Response(content="Login successful")
        response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,   # HTTPS only in production
        samesite="lax"
        )

        return response
    else:
        raise HTTPException(status_code=401, detail="wrong password err unauth ")

@UserRouter.post("/Logout")
async def Logout(response: Response):
    logout_delete_all_cookies(response)


#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html