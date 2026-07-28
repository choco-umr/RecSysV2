import logging
import pandas as pd

from .T2.T2_STEP1_FILE_CHECKS import STEP1_FILE_LOADING
from .T2.T2_STEP2_SCHEMA_VALIDATION import dataset_schema_validation
from .T2.T2_STEP4_USER_DERIVING import user_derivication

logger = logging.getLogger(__name__)

"""
run_etl_pipeline()
Purpose: Handles running the Whole ETL pipeline from start to finish
Steps: 
    1. Run first step fo the pipeline (File loading)
    2. Run second step of the pipeline (Schema validation)
    3. Run third step of the pipeline (call API Route to check for duplicates (deduplication)) ?
    4. Run fourth step of the pipeline (call API Route to upload to database) ?

Input: Temp file path, dataset type
Output: 
    1. Success - .
    2. Fail - .
"""


def run_etl_pipeline(file_path: str, dataset_type: str):
    logger.info("Datatset Upload Pipeline started")

    loaded_df = loading_file = STEP1_FILE_LOADING(file_path)

    validate_dataset_schema = dataset_schema_validation(loaded_df, dataset_type)
