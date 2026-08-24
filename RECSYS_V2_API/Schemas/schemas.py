from pydantic import BaseModel, Field, StrictStr, StrictInt, field_validator, model_validator
from typing import Literal, List
from uuid import UUID
from string import punctuation
from fastapi import Form
from Security.exceptions import *

from RECSYS_V2_ETL_PIPELINE.T2.Data_Schemas.schemas import available_news_categories, available_news_sub_categories

class User_Register_Input(BaseModel):
    Firstname: str = Field(min_length=2, max_length=10)
    Lastname: str = Field(min_length=2, max_length=10)
    Username: str = Field(min_length=2, max_length=25) # need to be unique  - add check
    Password: str = Field(min_length=5, max_length=10) 
    Gender: Literal["Male", "Female"]
    Age: int = Field(ge=10, le=100)
    PreferredCategories: List[str] = Field(default_factory=list)
    PreferredSubCategories: List[str] = Field(default_factory=list)

    @field_validator('Password', mode='after')
    @classmethod
    def password_check(cls, password: str):
        has_uppercase = any(c.isupper() for c in password)
        has_special_char = any(c in punctuation for c in password)

        if not has_uppercase:
            raise ValueError("Password must contain uppercase")
        if not has_special_char:
            raise ValueError("Password must special character")
        return password

    @field_validator('PreferredCategories', mode='after')
    @classmethod
    def validate_categories(cls, categories: List[str]):
        invalid = [c for c in categories if c not in available_news_categories]
        if invalid:
            raise ValueError(f"Invalid categories: {invalid}")
        return categories

    @field_validator('PreferredSubCategories', mode='after')
    @classmethod
    def validate_sub_categories(cls, sub_categories: List[str]):
        invalid = [s for s in sub_categories if s not in available_news_sub_categories]
        if invalid:
            raise ValueError(f"Invalid sub-categories: {invalid}")
        return sub_categories
    


class LoginInputSchema(BaseModel):
    Username: str = Field(default='Username here')
    Password: str = Field(default='Password here')


class AdminResearcher_Register_Input(BaseModel):
    Firstname: str = Field(default='John', min_length=2, max_length=10)
    Lastname: str = Field(default='Doe', min_length=2, max_length=10)
    Username: str = Field(min_length=2, max_length=25) # need to be unique  - add check
    Password: str = Field(min_length=5, max_length=10) 

    @field_validator('Password', mode='after')
    @classmethod
    def password_check(cls, password: str):
        has_uppercase = any(c.isupper() for c in password)
        has_special_char = any(c in punctuation for c in password)

        if not has_uppercase:
            raise ValueError("Password must contain uppercase")
        if not has_special_char:
            raise ValueError("Password must special character")
        
        return password

class Admin_Register_Input(BaseModel):
    Firstname: str = Field(default='John', min_length=2, max_length=10)
    Lastname: str = Field(default='Doe', min_length=2, max_length=10)
    Username: str = Field(min_length=2, max_length=25) # need to be unique  - add check
    Password: str = Field(min_length=5, max_length=10) 

    @field_validator('Password', mode='after')
    @classmethod
    def password_check(cls, password: str):
        has_uppercase = any(c.isupper() for c in password)
        has_special_char = any(c in punctuation for c in password)

        if not has_uppercase:
            raise ValueError("Password must contain uppercase")
        if not has_special_char:
            raise ValueError("Password must special character")
        
        return password


class AdminDeleteUser_Input(BaseModel):
    Username: str = Field(min_length=2, max_length=25) # need to be unique  - add check
    Usernameconfirm: str = Field(min_length=2, max_length=25) # need to be unique  - add check

    @model_validator(mode="after")
    def usernames_must_match(self):
        if self.Username != self.Usernameconfirm:
            raise ValueError("Both usernames must match")
        return self

class DatasetInputSchema(BaseModel):
    #datatset type
    DatasetType: str

    @model_validator(mode="after")
    def valid_dataset_type(self):
        if self.DatasetType.title() not in ["Interactions", "Content", "Derived_Users"]: #are we including derived users (after tom meeting)
            raise UserNotFound() #change to proper error
        return self

    @classmethod
    def as_form(cls, DatasetType: str = Form(...)):
        return cls(DatasetType=DatasetType)


class RecommendorInputSchema(BaseModel):
    #datatset type
    ALGORITHM_NAME: str

    # @model_validator(mode="after")
    # def valid_dataset_type(self):
    #     if not self.ALGORITHM_NAME.lower().startswith("R"):
    #         raise ValueError("ALGORITHM_NAME must start with 'R'")
    #     return self

    
class Store_interactions(BaseModel):
    ITEM_ID: str
    INTERACTION_TYPE: str
    
    @model_validator(mode="after")
    def valid_dataset_type(self):
        normalized = self.INTERACTION_TYPE.lower()
        if normalized not in ["like", "dislike", "report"]:
            raise ValueError("invalid interaction type")
        self.INTERACTION_TYPE = normalized
        return self

#notes
#ensure uuid is unique (0.001% can de dupe so check error handling)
#change value errors to hhtp errors?
