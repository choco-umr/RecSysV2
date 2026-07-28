import pandera.pandas as pa
import logging
from .Data_Schemas.schemas import dataset_schema_mapping
from ..exceptions import SchemaValidationError

logger = logging.getLogger(__name__)

"""
dataset_schema_validation()
Purpose: Validates dataset against relevant schema (dataset_schema_mapping)
Steps: 
    1. Fetch relevant schema for dataset type
    2. Pandera .validate schema, return validated dataframe

Input: Preprocessed dataset and dataset type
Output: 
    1. Success - schema_validated_dataset 
    2. Fail - Pandera SchemaError object

TO/DO
parse the schemavalidation error and return proeorly so user cans ee exact rows that are not to schema
"""

def dataset_schema_validation(df, dataset_type):
    logger.info("Schema validation started")

    schema = dataset_schema_mapping.get(dataset_type)
 
    try:
        schema_validated_dataset = schema.validate(df, lazy=True)
        logger.info("dataset schema validation complete")
        return schema_validated_dataset
    except (pa.errors.SchemaError, pa.errors.SchemaErrors) as e:
        logger.exception("Schema error") #CLEAN UP (SEE TO/DO)
        raise SchemaValidationError(e) #CLEAN UP (SEE TO/DO)


