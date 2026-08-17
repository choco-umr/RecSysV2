from streamlit import error, user

from Schemas.schemas import User_Register_Input, LoginInputSchema
from Database.models import Users, Researchers, Admins, Content
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select, distinct
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Database.db import get_db
from RECSYS_V2_RECOMMENDER import Base, RContentBasedFiltering

FrontendHelperRouter = APIRouter(prefix='/FrontendHelperRouter')

@FrontendHelperRouter.get("/GetCategories")
async def Register(db: Session = Depends(get_db)):

    Categories = db.execute(
    select(distinct(Content.CATEGORY)) #FOR NW GET CATGORIES FOMR AVAILABLE CONTENT NOT CTEGORIES FORM SCHEMAS SINCE SOME WONT BE THERE
    ).scalars().all()

    print(Categories)
    
    return Categories

@FrontendHelperRouter.get("/WhoAmI")
async def who_am_i(request: Request, db: Session = Depends(get_db)):
    return RBAC(request, db)