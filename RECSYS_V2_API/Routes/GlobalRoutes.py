from Schemas.schemas import LoginInputSchema
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Database.db import get_db

GlobalRouter = APIRouter(prefix='/GlobalRoutes')

@GlobalRouter.post("/login")
async def Login(LoginInput: LoginInputSchema, db: Session = Depends(get_db)):

    #Checking Username exists with tables
    for table in (Users, Researchers, Admins):
        UsernameExtract = select(table).where(table.USERNAME == LoginInput.Username)
        user = db.scalars(UsernameExtract).first()
    
        #if username exists then check password
        if user:
            if verify_password(user.PASSWORD, LoginInput.Password):
                access_token = create_jwt_token(str(user.USER_ID), str(user.USER_TYPE))
                response = Response(content="Login successful")
                response.set_cookie( key="access_token",value=access_token,httponly=True,secure=True)
                return response
            else:
                raise HTTPException(status_code=401, detail="wrong password err unauth ")
    
    #username not found so user doesnt exists regardless of password  
    raise HTTPException(status_code=404,detail="User not found")

@GlobalRouter.post("/Logout")
async def Logout(response: Response):
    logout_delete_all_cookies(response)