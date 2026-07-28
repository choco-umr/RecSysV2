import pandas as pd
import logging
import os
from ..exceptions import EmptyCSV
logger = logging.getLogger(__name__)

"""
STEP1_FILE LOADING()
Purpose: Ensure the locally saved file existing and is not corrupt
Steps:
    1. Locates the saved temp file created when a user uploads a dataset
    2. Ensure it existing
    3. Ensure its valid by reading first 5 lines

Input: Path (str) file path of temp file
Output:
    1. Sucess - Pandas Dataframe (df)
    2. Fail - Raises exception (e)

Notes:
Do we really need to check first 5 lines? or just ensure the file is there and leave that to schema validation?
"""

def STEP1_FILE_LOADING(path):
    logger.info("Locating uploaded file")

    #check path exists
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")

    logger.info(f"Located file sucessfully at: {path}")

    #check file is valid (read first 5 lines)
    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise EmptyCSV()
    except Exception as e:
        raise ValueError("Invalid CSV file: ", e)

    logger.info(f"File loaded, {len(df)} rows")

    return df