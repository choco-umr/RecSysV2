import logging
from abc import ABC
import numpy as np
import pandas as pd
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from Base import Recommender
from RECSYS_V2_API.Database.db import SessionLocal
from RECSYS_V2_API.Database.models import Interactions, Content

logger = logging.getLogger(__name__)

pd.set_option('display.max_colwidth', None)
np.set_printoptions(threshold=np.inf)

db = SessionLocal()

def load_data(db: Session):
    Interactions_data = Select(Interactions)
    Content_data = select(Content)

    Interactions_df = pd.read_sql(Interactions_data, db.bind)
    Content_df = pd.read_sql(Content_data, db.bind)

    return Content_df

    #load user preffered categories here

#

"""
Class CategoryMeanRecommender

Encapsulates the content based filtering recommendation approach.

Args:
    Recommender Abstract Base class
Returns:
    Ordered recommendations

Raises:
"""

class CategoryMeanRecommender(Recommender):
    def __init__(self):
        self.vectorizer = None
        self.categories_vectors = None
        self.mean_categories_vectors = None
        self.tfidf_matrix = None

    def fit(self, df):
        """
        Cleans data and generates mean scores for categoryies and TF-IDF scores for items.

        Args:
            Self
            Content_Df: Content Dataframe
            User_Df: User dataframe

        Returns:
            Mean category vectors (self.mean_categories_vectors)
            TF-IDF scores for all items (self.tfidf_matrix)

        Raises:
        """
        df = df.drop(columns=["DATASET_NAME", "TITLE", "ARTICLE_TYPE", "TIMESTAMP", "SUB_CATEGORY"]) #remove uneccesary columumns

        self.categories_vectors = {}
        self.mean_categories_vectors = {}
        self.vectorizer = TfidfVectorizer() #initalise TF-IDF vectorizer
        self.tfidf_matrix = {}

        self.tfidf_matrix  = self.vectorizer.fit_transform(df["ABSTRACT"]) #generate TF-IDF score for each item based on abstract


        for category in df['CATEGORY'].unique():
            idx = df[df["CATEGORY"] == category].index #retrieve unqiue categories (index) and create seperation
            self.categories_vectors[category] = self.tfidf_matrix[idx] # sorted TF-IDF into categories (idx)
            mean_vector = self.categories_vectors[category].mean(axis=0)
            self.mean_categories_vectors[category] = np.asarray(mean_vector) 

        return self

    def recommend(self, user_preffered_categories):
        """
        1. Generates similarities scores (similarity_scores)
        2. Sort scores by indicies (top_scores_indicies -> final_scores)
        3. Fetches relevant items_ids based on index within indicies (top_scores_indicies)

        Args:
            Self
            Content_Df: Content Dataframe
            User_Df: User dataframe

        Returns:
            Mean category vectors (self.mean_categories_vectors)
            TF-IDF scores for all items (self.tfidf_matrix)

        Raises:
        """

        mean_category_vector = self.mean_categories_vectors[user_preffered_categories]
        similarity_scores = cosine_similarity(self.tfidf_matrix, mean_category_vector).flatten()

        top_scores_indicies = similarity_scores.argsort()[::-1] #positions of top decending scores to refer back to original content df
        final_scores = similarity_scores[top_scores_indicies] # get value (scores) for each position in indiices array

        item_ids = df["ITEM_ID"].values   # or df.index.values, if that's your identifier
        recommended_ids = item_ids[top_scores_indicies] #get item ids based on score positions 

        print(recommended_ids)




#TO/DO
#within recommend() create loop to generate recommendations for multiple categories
#after this decided whihc to show etc ask tom