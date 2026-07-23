from Schemas.schemas import LoginInputSchema
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import verify_password, create_jwt_token, logout_delete_all_cookies, check_existing_jwt_token
from Database.db import get_db
from Security.exceptions import IncorrectLoginDetails, JWTFound

GlobalRouter = APIRouter(prefix='/GlobalRoutes')

@GlobalRouter.post("/login")
async def Login(request: Request, LoginInput: LoginInputSchema, db: Session = Depends(get_db)):

    #check for acess token first
    check_existing_jwt_token(request)

    #Checking Username exists with tables
    for table in (Users, Researchers, Admins):
        UsernameExtract = select(table).where(table.USERNAME == LoginInput.Username)
        user = db.scalars(UsernameExtract).first()
    
        #if username exists then check password
        if user:
            if verify_password(user.PASSWORD, LoginInput.Password):
                access_token = create_jwt_token(str(user.USER_ID))
                response = Response(content="Login successful")
                response.set_cookie( key="access_token",value=access_token,httponly=True,secure=True)
                return response
            else:
                raise IncorrectLoginDetails()
    
    #username not found so user doesnt exists regardless of password  
    raise IncorrectLoginDetails()

@GlobalRouter.post("/Logout")
async def Logout(response: Response):
    logout_delete_all_cookies(response)