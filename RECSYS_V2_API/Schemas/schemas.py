from pydantic import BaseModel, Field, StrictStr, StrictInt, field_validator, model_validator
from typing import Literal
from uuid import UUID
from string import punctuation
from fastapi import Form
from Security.exceptions import *

class User_Register_Input(BaseModel):
    Firstname: str = Field(default='John', min_length=2, max_length=10)
    Lastname: str = Field(default='Doe', min_length=2, max_length=10)
    Username: str = Field(min_length=2, max_length=25) # need to be unique  - add check
    Password: str = Field(min_length=5, max_length=10) 
    Gender: Literal["Male", "Female"]
    Age: int = Field(ge=10, le=100)

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



    
#notes
#ensure uuid is unique (0.001% can de dupe so check error handling)
#change value errors to hhtp errors?
