import pandas as pd
import logging
import os
logger = logging.getLogger(__name__)

#we downlaod the file form supbase to local api path /tmp
#then we cna run safety checks/etl pipeline

def initial_file_checks(path, dataset_type):
    logger.info("Safety checks started")

    # 1. Path check
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    
    if not os.path.exists(path):
        raise FileNotFoundError("File not found")

    if not path.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported")

    # 2. Size check (important for ETL safety)
    file_size_mb = os.path.getsize(path) / (1024 * 1024)

    if file_size_mb > 300:
        raise ValueError(f"File too large: {file_size_mb} MB")

    #logger.info(f"File size OK: {file_size_mb} MB")

    try:
        df = pd.read_csv(path, nrows=5)
    except Exception as e:
        raise ValueError("Invalid CSV file") from e

    logger.info("Safety checks passed")

    return True