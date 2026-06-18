import pandera.pandas as pa
import logging
from T2.Data_Schemas.schemas import dataset_schema_mapping

logger = logging.getLogger(__name__)

"""
dataset_schema_validation()
- Purpose: Validates dataset against relevant schmea
- Steps: 1. Fetch relevant schema (schemas.py), 2. Pandera .validate schema, return validated dataframe
- Input: Preprocessed dataset and dataset type
- Output: 
    Success - schema_validated_dataset 
    Fail - Pandera SchemaError object

- Raises:
- Notes
"""

def dataset_schema_validation(preprocessed_dataset, dataset_type):
    logger.info("dataset schema vlaidation started")

    schema = dataset_schema_mapping.get(dataset_type)

    if not schema:
        logger.error("Invalid dataset type exiting")
        return None
    else:
        try:
            schema_validated_dataset = schema.validate(preprocessed_dataset, lazy=True) #corece?
            logger.info("dataset schema validation complete")
            return schema_validated_dataset
        except (pa.errors.SchemaError, pa.errors.SchemaErrors) as e:
            logger.error("Schema error found")
            return e # correct?

