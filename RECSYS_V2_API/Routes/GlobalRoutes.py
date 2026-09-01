from fastapi import Depends, APIRouter, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from Schemas.schemas import login_input_schema

from Database.models import Users, Researchers, Admins
from Database.db import get_db

from Security.security import verify_password, create_jwt_token, logout_delete_all_cookies, check_existing_jwt_token
from Security.exceptions import incorrect_login_details, jwt_found

from config import expiry_time

global_router = APIRouter(prefix='/global_routes')

@global_router.post("/login")
async def login(request: Request, login_input: login_input_schema, db: Session = Depends(get_db)):

    check_existing_jwt_token(request) 

    role_map = {
        Users: "Users",
        Researchers: "Researchers",
        Admins: "Admins",
    }

    for table, role_name in role_map.items():
        username_extract = select(table).where(table.USERNAME == login_input.username)
        user = db.scalars(username_extract).first()

        if user:
            if verify_password(user.PASSWORD, login_input.password):
                access_token = create_jwt_token(str(user.USER_ID))
                response = JSONResponse(content={
                    "success": True,
                    "message": "Login successful",
                    "role": role_name
                })
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite="none",
                    max_age=int(expiry_time) * 60
                )
                return response
            else:
                raise incorrect_login_details()

    raise incorrect_login_details()


@global_router.post("/Logout")
async def logout(response: Response):
    logout_delete_all_cookies(response)


# NOTES
"""
- check_existing_jwt_token: confirm whether this check is applied consistently across all routes
- Cookie max_age is set from EXPIRY_TIME (minutes) to stay in sync with the JWT's "exp" claim
- Confirm the expiry on JWT actually works
"""