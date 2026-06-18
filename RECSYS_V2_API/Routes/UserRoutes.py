from Schemas.schemas import User_Register_Input, LoginInputSchema
from Database.models import Users
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, verify_jwt_token
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


@UserRouter.post("/user_jwt_data_test")
async def test_jwt_user_relative_data(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    decode_token = verify_jwt_token(token)
    print("TOKEN RETRIEVED and decoded", decode_token)
    print("user idddddd", decode_token["USER_ID"])
    return decode_token
    
    #generate s jwt token wiht the users UserID and UserType
    #redirect to relevant dashboard function


#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html