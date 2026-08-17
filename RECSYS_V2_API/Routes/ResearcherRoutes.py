import os
import shutil
from streamlit import error, user
from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input, DatasetInputSchema, RecommendorInputSchema
from Database.models import Users, Researchers, Admins, Content
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
import os
from pathlib import Path
import sys
import logging
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from RECSYS_V2_ETL_PIPELINE.run_pipeline import run_etl_pipeline
import os
logger = logging.getLogger(__name__)
from sqlalchemy import delete
ResearcherRouter = APIRouter(prefix='/ResearcherRoutes')

@ResearcherRouter.post("/DatasetUpload")
async def DatasetUpload(request: Request,file: UploadFile = File(...),DatasetInput: DatasetInputSchema = Depends(DatasetInputSchema.as_form),db: Session = Depends(get_db)):
    logger.info("Dataset upload process started")
    #how it works
    # run route
    #save file to local disk (temp folder in hosting server local filesystem)
    #validate file and run etl pipeline
    #if sucess upload to supbase (not coded yet)
    #delete temp file

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()


    logger.info("file validation started")
    FileValidator(file=file) #light validation before storing and proper validation
    logger.info("intitial file validaiton complete")


    try:
        logger.info("creating temp folder")
        #make temp folder to store file temporarily
        os.makedirs("temp", exist_ok=True)
        temp_file_path = os.path.join("temp",file.filename)
        logger.info("temp path created")
        
        # Save uploaded file to temp folder
        logger.info("saving file to temp folder")
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("temp file saved")

        #Run ETL pipeline on temp file
        result = run_etl_pipeline(
            file_path=temp_file_path,
            dataset_type=DatasetInput.DatasetType
        )
        return {"message": "Dataset processed successfully","result": result}

    #save csv file now

    finally:
        # remove temp file 
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


#upload recommender algorithm - aks tom for a single file type do other algos need other file types etc?

#choose reocmmder and will run evrytime the reocmmedations are generaed (once a day at 12 or someting)
@ResearcherRouter.post("/ChooseRecommenderAlgorithm")
def ChooseRecommenderAlgorithm(request: Request,RecommenderNameInput: RecommenderInputSchema = Depends(DatasetInputSchema.as_form),db: Session = Depends(get_db)):

    folder = "/RECSYS_V2_RECOMMENDER"
    available_recommenders = []
    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)
        print(name, ext)
        if name.startswith("-r") and ext == ".py":
            available_recommenders.append(name)
        else:
            pass

    if RecommenderNameInput in available_recommenders:
        #clear db then insert db with alogirthm name and currentyl active
        #just for the first insert we delete the change code to just edit

        db.execute(delete(models.RecommendorAlgorithms))
        db.commit()

        Selected_algorithm = RecommendorAlgorithms(
             ALGORITHM_NAME = RecommenderNameInput,
             CURRENTLY_ACTIVE = "Yes"
            )

        db.add(Selected_algorithm)
        db.commit()
        db.refresh(Selected_algorithm)

    else:
        print("error rec gen not found")




#dashboard analytics


#check repo folder locally /recommder
#find all files wiht beginning wiht -r
 #choose the selected algo and set it within RecommendorAlgorithms.CURRENTLY_ACTIVE
    
# db.add(dataset)
# db.commit()