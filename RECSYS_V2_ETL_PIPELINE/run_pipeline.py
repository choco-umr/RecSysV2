import logging
import pandas as pd

from T2.T2_STEP1_FILE_CHECKS import initial_file_checks #need to add supbase download function in here too in whihc we pass into next func
from T2.T2_STEP2_PREPROCESSING import etl_preprocessing
from T2.T2_STEP3_SCHEMA_VALIDATION import dataset_schema_validation
from T2.T2_STEP4_USER_DERIVING import user_derivication


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() - '%(message)s'",
    force=True)

"""
run_etl_pipeline()
- Purpose: Kick starts ETL pipeline upon Dataset upload
- Steps: 1. Preprocess Data, 2. Validate Schema, 3. x, 4. x, 5.
- Input: Dataset & Dataset Type
- Output: 
    Success - Uploaded Data / Cleaned dataset?
    Fail - 
- Raises:
- Notes
"""
def run_etl_pipeline(df, dataset_type):
    logger.info("ETL Pipeline started")

    inital_verification_steps = initial_file_checks(path, dataset_type)
    preprocessed_dataset = etl_preprocessing(df) # temporarily pass in df manually, later on it will come from preok giv eme instruciton i want toious func
    schema_validated_dataset = dataset_schema_validation(preprocessed_dataset, dataset_type)
    
    if dataset_type == "Interactions":
        user_derivication_process = user_derivication(schema_validated_dataset, dataset_type) # return both user derived df and schema validated df
    else:
        pass




path = r"C:\Users\umr\Desktop\WORK\RECSYS_V2_ETL_PIPELINE\T1MindInteractionsTOP50.csv"
dataset_type = "Interactions"
df = pd.read_csv(path)
run_etl_pipeline(df, dataset_type)


#Download file from Supabase
# Save it temporarily (usually /tmp/)
# Run safety checks
# Load into pandas
# Run ETL
# Insert into DB
# Delete temp file (optional but recommended)