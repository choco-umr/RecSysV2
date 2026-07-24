from streamlit import error, user

from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input, DatasetInputSchema
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Database.db import get_db
from Security.exceptions import UserNotAuthorized, InvalidFiletype
from Security.security import FileValidator
from fastapi import FastAPI, File, UploadFile, File, Form, UploadFile
from typing import Annotated


ResearcherRouter = APIRouter(prefix='/ResearcherRoutes')


#datasetupload
#researcher passes in dataset type alongside data matching the relevant dataset schema which starts the pipeline


from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

class DatasetInputSchema(BaseModel):
    DatasetType: str

    @field_validator("DatasetType")
    @classmethod
    def validate_dataset_type(cls, value: str) -> str:
        valid_types = {
            "interactions",
            "content",
            "derived_users",
            "video",
        }

        if value.lower() not in valid_types:
            raise ValueError(
                f"DatasetType must be one of: {', '.join(valid_types)}"
            )

        return value

    @classmethod
    def as_form(
        cls,
        DatasetType: str = Form(...),
    ):
        return cls(DatasetType=DatasetType)


@ResearcherRouter.post("/DatasetUpload")
async def DatasetUpload(file: UploadFile = File(...), DatasetInput: DatasetInputSchema = Depends(DatasetInputSchema.as_form),db: Session = Depends(get_db),):
    FileValidator(file=file,max_size_bytes=5 * 1024 * 1024 * 1024)  # file vaidator