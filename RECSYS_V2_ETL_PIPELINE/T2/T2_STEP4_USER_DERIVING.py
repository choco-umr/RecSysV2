#this step invovles deriving user data from interaction uploads. 
#We cnanto derive users from news uploads only so they need to be interaction uploadsa
import pandas as pd
import pandera as pa
import logging

logger = logging.getLogger(__name__)


def user_derivication(schema_validated_dataset, dataset_type):
    logger.info("User derivication started")

    #getting unique users
    df = schema_validated_dataset
    unique_users = df['USER_ID'].unique()

    #check if userid existing in db already

    #if not already existing
    #write to sql alchemy model using below way

    #every unique user id in dataset that isnt already in the users table, we create a databae additon for it.
    
    #userid from the original dataset
    #Username will be original_dataset_name + _ 15 random chars (a-z,A-Z,1-9)
    #Age will be will be random - open to change
    #is child_depenant on age column
    #gender will be random - open to change
    #country will be the UK as all interactions we will work with will be UK based

    #rows to remove from documentation
    #Subscription

    #Workflow for this func > Data extracted and added (age, gender) etc > SQLalchemy verification > additon to db (Next func)














