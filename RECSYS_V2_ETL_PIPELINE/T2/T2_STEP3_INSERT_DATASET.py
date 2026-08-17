from fastapi import Depends
from sqlalchemy.orm import Session
import pandas as pd
import logging
from Database.models import Interactions, Content
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

def remove_duplicates_and_insert(df, dataset_type, db: Session):
    logger.info("Deduplication started")
    if dataset_type == "Interactions":
        stmt = insert(Interactions).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_nothing(
            index_elements=[
                "DATASET_NAME", "USER_ID", "ITEM_ID", "TIMESTAMP", "INTERACTION_TYPE",
            ]
        )
        try:
            result = db.execute(stmt)
            db.commit()
            logger.info(f"Inserted {result.rowcount} rows")
            return result.rowcount
        except Exception as e:
            db.rollback()
            logger.error(f"Insert failed: {type(e).__name__}: {e}")
            raise

    elif dataset_type == "Content":
        stmt = insert(Content).values(df.to_dict(orient="records"))
        stmt = stmt.on_conflict_do_nothing(
        index_elements=[
            "DATASET_NAME", "TITLE", "CATEGORY", "SUB_CATEGORY", "ABSTRACT", "TIMESTAMP", "ARTICLE_TYPE"
        ]
    )
        
        try:
            result = db.execute(stmt) 
            db.commit()
            logger.info(f"Inserted {result.rowcount} rows")
            return result.rowcount
        except Exception as e:
            db.rollback()
            logger.error(f"Insert failed: {type(e).__name__}: {e}")
            raise
    else:
        logger.error(f"Invalid dataset type: {dataset_type}")
        raise ValueError(f"Invalid dataset type: {dataset_type}")



"""
what we need to solve
#A way to check for duplicate sin an efficent amnner for every line in the df

#this is good a good issue to use for one of the ksbs
#how to check for duplicates in an lowest big 0 time.

#We can just check each row one by one since that is loads of db queries
#we can pull in the whole database since there could worst case be millions of rows
#we need to find the ebst solution to this

esentially a better way to upload datasets instead of line by line

"""