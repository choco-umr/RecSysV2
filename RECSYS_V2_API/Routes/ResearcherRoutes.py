import os
import shutil
from streamlit import error, user
from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input, DatasetInputSchema, RecommendorInputSchema
from Database.models import Users, Researchers, Admins, Content, RecommendorAlgorithms, Interactions
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
import datetime
from datetime import datetime, timedelta
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import extract

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
async def ChooseRecommenderAlgorithm(request: Request,RecommenderNameInput: RecommendorInputSchema,db: Session = Depends(get_db)):
    
    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()

    folder = ROOT / "RECSYS_V2_RECOMMENDER"
    available_recommenders = []
    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)
        if name.startswith("R") and ext == ".py":
            available_recommenders.append(name)
            print("available recommders: ", available_recommenders)
        else:
            pass

    if RecommenderNameInput.ALGORITHM_NAME in available_recommenders:

        CurrentActiveAlgorithm = db.execute(
        select(RecommendorAlgorithms).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == True)
    ).scalar_one_or_none()

        if CurrentActiveAlgorithm:
             CurrentActiveAlgorithm.CURRENTLY_ACTIVE = False
             CurrentActiveAlgorithm.TIMESTAMP_END = datetime.datetime.now()


        Selected_algorithm = RecommendorAlgorithms(
             ALGORITHM_NAME = RecommenderNameInput.ALGORITHM_NAME,
             CURRENTLY_ACTIVE = True,
             TIMESTAMP_START = datetime.datetime.now(),
             TIMESTAMP_END = None
            )

        db.add(Selected_algorithm)
        db.commit()
        db.refresh(Selected_algorithm)

        return {"success": True, "active_algorithm": Selected_algorithm.ALGORITHM_NAME}


    else:
        raise HTTPException(status_code=404, detail="Recommender algorithm not found")




#dashboard analytics

@ResearcherRouter.get("/IntractionTypeBreakdown")
async def IntractionTypeBreakdown(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()

    interaction_type_counts = db.execute(
    select(Interactions.INTERACTION_TYPE, func.count())
    .group_by(Interactions.INTERACTION_TYPE)
    ).all()

    total_interactions = sum(count for _, count in interaction_type_counts)

    interaction_type_breakdown = [
        {
            "type": interaction_type,
            "count": count,
            "percentage": round((count / total_interactions) * 100, 1) if total_interactions > 0 else 0
        }
        for interaction_type, count in interaction_type_counts
    ]

    return interaction_type_breakdown



@ResearcherRouter.get("/InteractionDensity")
async def InteractionDensity(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()

    #average number of interactions per item

    #1. get all items from intercations (items that actually have interactions)
    #2. total interactions count / count of items ith interactions
    #3 percentage of items with no interactions = total items in content − items with interactions. Then: percentage = (items with no interactions ÷ total items in content) × 100.

    Interaction_count = db.execute(
    select(func.count()).select_from(Interactions)
    ).scalar_one()

    items_with_interactions = db.execute(
    select(Interactions.ITEM_ID, func.count())
    .group_by(Interactions.ITEM_ID)
    ).all()

    count_of_items_with_interactions = len(items_with_interactions)

    average_interactions_per_item = Interaction_count / count_of_items_with_interactions

    Content_count = db.execute(
    select(func.count()).select_from(Content)
    ).scalar_one()

    no_interaction_items_count =  Content_count - count_of_items_with_interactions

    no_interaction_items_percentage = (no_interaction_items_count / Content_count) * 100

    return {
    "success": True,
    "average_interactions_per_item": average_interactions_per_item,
    "no_interaction_items_percentage": no_interaction_items_percentage
}


@ResearcherRouter.get("/InteractionDataTimeRange")
async def InteractionDataTimeRange(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()

    Interaction_volume_by_week = db.execute(
    select(
        func.date_trunc('week', Interactions.TIMESTAMP).label('week'),
        func.count()
        )
        .group_by('week')
        .order_by('week')
    ).all()

    Interaction_volume_by_day = db.execute(
    select(
        func.date_trunc('day', Interactions.TIMESTAMP).label('day'),
        func.count()
        )
        .group_by('day')
        .order_by('day')
    ).all()

    return {
    "success": True,
    "interaction_volume_by_week": [{"week": w.isoformat(), "count": c} for w, c in Interaction_volume_by_week],
    "interaction_volume_by_day": [{"day": d.isoformat(), "count": c} for d, c in Interaction_volume_by_day]
}



# recommendation algorithm tracking

@ResearcherRouter.get("/RecommendorAlgorithmsInteractionStatistics")
async def RecommendorAlgorithmsStatistics(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()

    UNIQUE_ALGORITHM_LIST = db.execute(
        select(RecommendorAlgorithms.ALGORITHM_NAME).distinct()
    ).scalars().all()

    for algorithm in UNIQUE_ALGORITHM_LIST:

        interaction_type_counts = db.execute(
            select(Interactions.INTERACTION_TYPE, func.count())
            .where(Interactions.ALGORITHM_USED == algorithm)
            .group_by(Interactions.INTERACTION_TYPE)
            ).all()

    total_interactions = sum(count for _, count in interaction_type_counts)


    return total_interactions


#content distribution

@ResearcherRouter.get("/Content_distribution")
async def Content_distribution(request: Request,db: Session = Depends(get_db)):
    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise UserNotAuthorized()


    category_counts = db.execute(
        select(Content.CATEGORY, func.count())
        .group_by(Content.CATEGORY)
    ).all()

    subcategory_counts = db.execute(
        select(Content.SUB_CATEGORY, func.count())
        .group_by(Content.SUB_CATEGORY)
    ).all()

    article_type_counts = db.execute(
        select(Content.ARTICLE_TYPE, func.count())
        .group_by(Content.ARTICLE_TYPE)
    ).all()


    return {
        "category_counts": [{"category": c, "count": n} for c, n in category_counts],
        "subcategory_counts": [{"subcategory": s, "count": n} for s, n in subcategory_counts],
        "article_type_counts": [{"article_type": a, "count": n} for a, n in article_type_counts]
    }
