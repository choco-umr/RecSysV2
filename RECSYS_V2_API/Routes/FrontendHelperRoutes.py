from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct

from Schemas.schemas import user_register_input, login_input_schema

from Database.models import Users, Researchers, Admins, Content
from Database.db import get_db

from Security.security import hash_password, generate_user_id, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC

frontend_helper_router = APIRouter(prefix='/frontend_helper_router')

@frontend_helper_router.get("/get_categories")
async def register(db: Session = Depends(get_db)):

    categories = db.execute(
    select(distinct(Content.CATEGORY))
    ).scalars().all()
    
    return categories

@frontend_helper_router.get("/who_am_i")
async def who_am_i(request: Request, db: Session = Depends(get_db)):
    return RBAC(request, db)


# NOTES
"""
- get_categories: currently pulling categories from available Content, not from Schemas — some categories may be missing as a result. Revisit later.
"""