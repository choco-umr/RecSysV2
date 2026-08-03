from fastapi import Depends
from sqlalchemy.orm import Session
import pandas as pd
import logging
from Database.models import Interactions
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)

def remove_duplicates(df, dataset_type, db: Session):
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


"""
what we need to solve
#A way to check for duplicate sin an efficent amnner for every line in the df

#this is good a good issue to use for one of the ksbs
#how to check for duplicates in an lowest big 0 time.

#We can just check each row one by one since that is loads of db queries
#we can pull in the whole database since there could worst case be millions of rows
#we need to find the ebst solution to this


DF Schema:

InteractionsDataSchema = pa.DataFrameSchema({
    "DATASET_NAME": pa.Column(str, pa.Check.str_length(min_value=3, max_value=25)),
    "USER_ID": pa.Column(str, pa.Check.str_length(min_value=2, max_value=25)), #imported intercations datasets will have thir own users di in it
    "ITEM_ID": pa.Column(str, pa.Check.str_length(min_value=2, max_value=10)), #relationship checking
    "TIMESTAMP": pa.Column(str), #check format of mind and ebnerd
    "INTERACTION_TYPE": pa.Column(str, pa.Check.isin(available_interaction_types)),
    "READ_TIME": pa.Column(float, pa.Check.in_range(0, 18000), nullable=True), #In seconds
    "SCROLL_PERCENTAGE": pa.Column(float, pa.Check.in_range(0.0, 100.0), nullable=True)
}, strict="filter", ordered=True)


Model:

class Interactions(Base):
    __tablename__ = "Interactions"
    DATASET_NAME = Column(String, nullable=False)
    INTERACTION_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) #has to be str and not uuid since items cna be upoaded and they wont be uuids

    USER_ID = Column(String, nullable=False) #has to be str and not uuid since items cna be upoaded and they wont be uuids
    ITEM_ID = Column(String, nullable=False) #has to be str and not uuid since items cna be upoaded and they wont be uuids

    TIMESTAMP = Column(DateTime)
    INTERACTION_TYPE = Column(String, nullable=False)
    READ_TIME = Column(Float, nullable=True)
    SCROLL_PERCENTAGE = Column(Float, nullable=True)


"""