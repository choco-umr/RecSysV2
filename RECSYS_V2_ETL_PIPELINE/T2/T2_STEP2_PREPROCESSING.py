import pandas as pd
import logging
#for now we only handle csv's
logger = logging.getLogger(__name__)


def etl_preprocessing(df):
    logger.info("Preprocessing started")
    df.columns = df.columns.map(str.upper) #Capitalises all column names
    df.columns = df.columns.str.strip().str.replace(" ", "_") #removing beginning and trailing whitepaces
    df = df.dropna(how="all") #drop completely empty rows 
    logger.info("dataset preprocess complete")

    return df

