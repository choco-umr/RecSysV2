import datetime
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, Response, Request, FastAPI, File, UploadFile, Form
from sqlalchemy import select, delete, create_engine, func
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import extract

from Schemas.schemas import admin_researcher_register_input, admin_register_input, dataset_input_schema, recommendor_input_schema

from Database.models import Users, Researchers, Admins, Content, RecommendorAlgorithms, Interactions
from Database.db import get_db

from Security.security import hash_password, generate_user_id, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC, file_validator
from Security.exceptions import user_not_authorized, invalid_file_type

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from RECSYS_V2_ETL_PIPELINE.run_pipeline import run_etl_pipeline

logger = logging.getLogger(__name__)

researcher_router = APIRouter(prefix='/researcher_routes')

@researcher_router.post("/dataset_upload")
async def dataset_upload(request: Request,file: UploadFile = File(...), dataset_input: dataset_input_schema = Depends(dataset_input_schema.as_form),db: Session = Depends(get_db)):
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
        raise user_not_authorized()


    logger.info("file validation started")
    file_validator(file=file) #light validation before storing and proper validation
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
            dataset_type=dataset_input.dataset_type
        )
        return {"message": "Dataset processed successfully","result": result}

    #save csv file now

    finally:
        # remove temp file 
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@researcher_router.post("/choose_recommender_algorithm")
async def choose_recommender_algorithm(request: Request, recommender_name_input: recommendor_input_schema, db: Session = Depends(get_db)):
    
    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise user_not_authorized()

    folder = ROOT / "RECSYS_V2_RECOMMENDER"
    available_recommenders = []
    for file in os.listdir(folder):
        name, ext = os.path.splitext(file)
        if name.startswith("R") and ext == ".py":
            available_recommenders.append(name)
            print("available recommders: ", available_recommenders)
        else:
            pass

    if recommender_name_input.algorithm_name in available_recommenders:

        current_active_algorithm = db.execute(
        select(RecommendorAlgorithms).where(RecommendorAlgorithms.CURRENTLY_ACTIVE == True)
    ).scalar_one_or_none()

        if current_active_algorithm:
             current_active_algorithm.CURRENTLY_ACTIVE = False
             current_active_algorithm.TIMESTAMP_END = datetime.datetime.now()

        # ALGORITHM_NAME is the primary key, so re-selecting an algorithm that
        # already has a row (e.g. the one just marked inactive above) must
        # update that row instead of inserting a duplicate primary key.
        existing_algorithm_row = db.execute(
            select(RecommendorAlgorithms).where(RecommendorAlgorithms.ALGORITHM_NAME == recommender_name_input.algorithm_name)
        ).scalar_one_or_none()

        if existing_algorithm_row:
            existing_algorithm_row.CURRENTLY_ACTIVE = True
            existing_algorithm_row.TIMESTAMP_START = datetime.datetime.now()
            existing_algorithm_row.TIMESTAMP_END = None
            selected_algorithm = existing_algorithm_row
        else:
            selected_algorithm = RecommendorAlgorithms(
                 ALGORITHM_NAME = recommender_name_input.algorithm_name,
                 CURRENTLY_ACTIVE = True,
                 TIMESTAMP_START = datetime.datetime.now(),
                 TIMESTAMP_END = None
                )
            db.add(selected_algorithm)

        db.commit()
        db.refresh(selected_algorithm)

        return {"success": True, "active_algorithm": selected_algorithm.ALGORITHM_NAME}

    else:
        raise HTTPException(status_code=404, detail="Recommender algorithm not found") #clean up httpeception




#dashboard analytics
@researcher_router.get("/intraction_type_breakdown")
async def intraction_type_breakdown(request: Request, db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise user_not_authorized()

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



@researcher_router.get("/interaction_density")
async def interaction_density(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise user_not_authorized()

    #average number of interactions per item

    #1. get all items from intercations (items that actually have interactions)
    #2. total interactions count / count of items ith interactions
    #3 percentage of items with no interactions = total items in content − items with interactions. Then: percentage = (items with no interactions ÷ total items in content) × 100.

    interaction_count = db.execute(
    select(func.count()).select_from(Interactions)
    ).scalar_one()

    items_with_interactions = db.execute(
    select(Interactions.ITEM_ID, func.count())
    .group_by(Interactions.ITEM_ID)
    ).all()

    count_of_items_with_interactions = len(items_with_interactions)

    average_interactions_per_item = interaction_count / count_of_items_with_interactions

    content_count = db.execute(
    select(func.count()).select_from(Content)
    ).scalar_one()

    no_interaction_items_count =  content_count - count_of_items_with_interactions

    no_interaction_items_percentage = (no_interaction_items_count / content_count) * 100

    return {
    "success": True,
    "average_interactions_per_item": average_interactions_per_item,
    "no_interaction_items_percentage": no_interaction_items_percentage
}


@researcher_router.get("/interaction_data_time_range")
async def interaction_data_time_range(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise user_not_authorized()

    interaction_volume_by_week = db.execute(
    select(
        func.date_trunc('week', Interactions.TIMESTAMP).label('week'),
        func.count()
        )
        .group_by('week')
        .order_by('week')
    ).all()

    interaction_volume_by_day = db.execute(
    select(
        func.date_trunc('day', Interactions.TIMESTAMP).label('day'),
        func.count()
        )
        .group_by('day')
        .order_by('day')
    ).all()

    return {
    "success": True,
    "interaction_volume_by_week": [{"week": w.isoformat(), "count": c} for w, c in interaction_volume_by_week],
    "interaction_volume_by_day": [{"day": d.isoformat(), "count": c} for d, c in interaction_volume_by_day]
}



# recommendation algorithm tracking

@researcher_router.get("/recommendor_algorithms_interaction_statistics")
async def recommendor_algorithms_statistics(request: Request,db: Session = Depends(get_db)):

    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise user_not_authorized()

    unique_algorithms_list = db.execute(
        select(RecommendorAlgorithms.ALGORITHM_NAME).distinct()
    ).scalars().all()

    algorithm_statistics = []
    for algorithm in unique_algorithms_list:

        interaction_type_counts = db.execute(
            select(Interactions.INTERACTION_TYPE, func.count())
            .where(Interactions.ALGORITHM_USED == algorithm)
            .group_by(Interactions.INTERACTION_TYPE)
            ).all()

        total_interactions = sum(count for _, count in interaction_type_counts)

        algorithm_statistics.append({
            "algorithm": algorithm,
            "total_interactions": total_interactions,
            "breakdown": [{"type": t, "count": c} for t, c in interaction_type_counts]
        })

    return algorithm_statistics


#content distribution

@researcher_router.get("/Content_distribution")
async def Content_distribution(request: Request,db: Session = Depends(get_db)):
    rbac_result = RBAC(request, db)
    user_type = rbac_result["role"]
    user_id = rbac_result["user_id"]

    if user_type != "Researchers":
        raise user_not_authorized()


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


# NOTES
"""
- properly comment all functions like etl pipeline functions (check step 1 file loading notes)
"""