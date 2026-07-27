import os
import shutil

from streamlit import error, user

from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input, DatasetInputSchema
from Database.models import Users, Researchers, Admins, Content, Dataset_Upload_Tracking
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC, FileValidator
from Database.db import get_db
from Security.exceptions import UserNotAuthorized, InvalidFiletype, SchemaValidationError
from Security.security import FileValidator
from fastapi import FastAPI, File, UploadFile, File, Form, UploadFile
from typing import Annotated
import datetime
import os
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from RECSYS_V2_ETL_PIPELINE import run_pipeline


ResearcherRouter = APIRouter(prefix='/ResearcherRoutes')


@ResearcherRouter.post("/DatasetUpload")
async def DatasetUpload(request: Request, file: UploadFile = File(...), DatasetInput: DatasetInputSchema = Depends(DatasetInputSchema.as_form),db: Session = Depends(get_db),):
    FileValidator(file=file,max_size_bytes=5 * 1024 * 1024 * 1024)  # file validator

    user_type, user_id = RBAC(request, db)
    if user_type != "Researchers":
        raise UserNotAuthorized()

    FileValidator(file=file)

    os.makedirs("temp", exist_ok=True)
    temp_file_path = f"temp/{file.filename}"

import os
import shutil

from RECSYS_V2_ETL_PIPELINE.run_pipeline import run_etl_pipeline


@ResearcherRouter.post("/DatasetUpload")
async def DatasetUpload(request: Request,file: UploadFile = File(...),DatasetInput: DatasetInputSchema = Depends(DatasetInputSchema.as_form),db: Session = Depends(get_db),):
    #how it works
    # run route
    #save file to local disk (temp folder in hosting server local filesystem)
    #validate file and run etl pipeline
    #if sucess upload to supbase (not coded yet)
    #delete temp file

    user_type, user_id = RBAC(request, db)
    if user_type != "Researchers":
        raise UserNotAuthorized()

    FileValidator(file=file)

    try:
        #make temp folder to store file temporarily
        os.makedirs("temp", exist_ok=True)
        temp_file_path = os.path.join("temp",file.filename)
        
        # Save uploaded file to temp folder
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run ETL pipeline on temp file
        result = run_etl_pipeline(
            file_path=temp_file_path,
            dataset_type=DatasetInput.dataset_type
        )
        return {"message": "Dataset processed successfully","result": result}

    #save csv file now

    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            

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

    #once checks passed we need 2 uploads
    #1. to dataset upload tracking with metadata
    #2. the data to the supabase storage
    
# db.add(dataset)
# db.commit()