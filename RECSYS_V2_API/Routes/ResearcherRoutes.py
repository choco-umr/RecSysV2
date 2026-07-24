from streamlit import error, user

from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input, DatasetInputSchema
from Database.models import Users, Researchers, Admins, Content, Dataset_Upload_Tracking
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC, FileValidator
from Database.db import get_db
from Security.exceptions import UserNotAuthorized, InvalidFiletype
from Security.security import FileValidator
from fastapi import FastAPI, File, UploadFile, File, Form, UploadFile
from typing import Annotated
import datetime

ResearcherRouter = APIRouter(prefix='/ResearcherRoutes')


@ResearcherRouter.post("/DatasetUpload")
async def DatasetUpload(request: Request, file: UploadFile = File(...), DatasetInput: DatasetInputSchema = Depends(DatasetInputSchema.as_form),db: Session = Depends(get_db),):
    FileValidator(file=file,max_size_bytes=5 * 1024 * 1024 * 1024)  # file validator

    #once checks passed we need 2 uploads
    #1. to dataset upload tracking with metadata
    #2. the data to the supabase storage

    user_type, user_id = RBAC(request, db)
    if user_type != "Researchers":
        raise UserNotAuthorized()
    
    #to/do
    #pass file into securities FileValidator
    # rename file to something
    #upload file to supbase storage

    track_dataset = Dataset_Upload_Tracking(
        FILENAME=file.filename,
        DATASET_TYPE=DatasetInput.DatasetType,
        UPLOADED_BY_USER_ID=user_id,
        UPLOADED_AT=datetime.utcnow(),
        FILE_SIZE=file.size,
        ROW_COUNT=None,
        UPLOAD_STATUS="Uploaded"
    )

# db.add(dataset)
# db.commit()