from pydantic import BaseModel, Field, StrictStr, StrictInt, field_validator
from typing import Literal
from uuid import UUID
from string import punctuation


class User_Register_Input(BaseModel):
    Firstname: str = Field(default='John', min_length=2, max_length=10)
    Lastname: str = Field(default='Doe', min_length=2, max_length=10)
    Username: str = Field(min_length=2, max_length=10) # need to be unique  - add check
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


    
#notes
#ensure uuid is unique (0.001% can de dupe so check error handling)
#change value errors to hhtp errors?