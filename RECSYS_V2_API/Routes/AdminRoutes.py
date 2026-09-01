from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select

from Schemas.schemas import admin_researcher_register_input, admin_register_input, admin_delete_user_input

from Database.models import Users, Researchers, Admins
from Database.db import get_db

from Security.security import hash_password, generate_user_id, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Security.exceptions import user_not_authorized, user_not_found

admin_router = APIRouter(prefix='/admin_routes')

@admin_router.post("/admin_register")
async def admin_register(request: Request, User: admin_register_input, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Admins":
        raise user_not_authorized()

    dupe_username_check = db.execute(
        select(Admins).where(Admins.USERNAME == User.username)
    ).scalar_one_or_none()
    
    if dupe_username_check is not None:
        raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
    else:
        generated_user_id = generate_user_id()
        hashed_password = hash_password(User.password)

        new_user = Admins(
            USER_ID = generated_user_id,
            FIRST_NAME=User.firstname,
            LAST_NAME=User.lastname,
            USERNAME=User.username,
            PASSWORD=hashed_password,
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "USER_ID": new_user.USER_ID,
            "FIRST_NAME": new_user.FIRST_NAME,
            "LAST_NAME": new_user.LAST_NAME,
            "USERNAME": new_user.USERNAME,
        }

@admin_router.post("/researcher_register")
async def admin_researcher_egister(request: Request, User: admin_researcher_register_input, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]
    if user_type != "Admins":
        raise user_not_authorized()

    dupe_username_check = db.execute(
        select(Researchers).where(Researchers.USERNAME == User.username)
    ).scalar_one_or_none()

    if dupe_username_check is not None:
        raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
    else:
        generated_user_id = generate_user_id()
        hashed_password = hash_password(User.password)

        new_user = Researchers(
            USER_ID = generated_user_id,
            FIRST_NAME=User.firstname,
            LAST_NAME=User.lastname,
            USERNAME=User.username,
            PASSWORD=hashed_password,
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "USER_ID": new_user.USER_ID,
            "FIRST_NAME": new_user.FIRST_NAME,
            "LAST_NAME": new_user.LAST_NAME,
            "USERNAME": new_user.USERNAME,
        }

@admin_router.post("/delete_user")
async def DeleteUser(request: Request, User: admin_delete_user_input, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]
    if user_type != "Admins":
        raise user_not_authorized()


    user = None
    for table in (Users, Researchers, Admins):
        stmt = select(table).where(table.USERNAME == User.username)
        found = db.scalars(stmt).first()

        if found:
            user = found
            break

    if not user:
        raise user_not_found()

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}




# NOTES
"""
- TODO: clean up all HTTPExceptions (standardize error handling)
"""