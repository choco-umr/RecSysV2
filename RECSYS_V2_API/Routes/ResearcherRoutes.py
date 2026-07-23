from streamlit import error, user

from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Database.db import get_db
from Security.exceptions import UserNotAuthorized


ResearcherRouter = APIRouter(prefix='/ResearcherRoutes')


#datasetupload
#researcher passes in dataset type alongside data matching the relevant dataset schema which starts the pipeline
