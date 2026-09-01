from string import punctuation
from typing import Literal, List
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, Field, StrictStr, StrictInt, field_validator, model_validator

from Security.exceptions import *

class user_register_input(BaseModel):
    firstname: str = Field(min_length=2, max_length=10)
    lastname: str = Field(min_length=2, max_length=10)
    username: str = Field(min_length=2, max_length=25)
    password: str = Field(min_length=5, max_length=10) 
    gender: Literal["Male", "Female"]
    age: int = Field(ge=10, le=100)
    preferred_categories: List[str] = Field(default_factory=list)
    preferred_sub_categories: List[str] = Field(default_factory=list)

    @field_validator('password', mode='after')
    @classmethod
    def password_check(cls, password: str):
        has_uppercase = any(c.isupper() for c in password)
        has_special_char = any(c in punctuation for c in password)

        if not has_uppercase:
            raise ValueError("Password must contain uppercase")
        if not has_special_char:
            raise ValueError("Password must special character")
        return password

        

class login_input_schema(BaseModel):
    username: str = Field(default='Username here')
    password: str = Field(default='Password here')


class admin_researcher_register_input(BaseModel):
    firstname: str = Field(default='John', min_length=2, max_length=10)
    lastname: str = Field(default='Doe', min_length=2, max_length=10)
    username: str = Field(min_length=2, max_length=25)
    password: str = Field(min_length=5, max_length=10) 

    @field_validator('password', mode='after')
    @classmethod
    def password_check(cls, password: str):
        has_uppercase = any(c.isupper() for c in password)
        has_special_char = any(c in punctuation for c in password)

        if not has_uppercase:
            raise ValueError("Password must contain uppercase")
        if not has_special_char:
            raise ValueError("Password must special character")
        
        return password

class admin_register_input(BaseModel):
    firstname: str = Field(default='John', min_length=2, max_length=10)
    lastname: str = Field(default='Doe', min_length=2, max_length=10)
    username: str = Field(min_length=2, max_length=25)
    password: str = Field(min_length=5, max_length=10) 

    @field_validator('password', mode='after')
    @classmethod
    def password_check(cls, password: str):
        has_uppercase = any(c.isupper() for c in password)
        has_special_char = any(c in punctuation for c in password)

        if not has_uppercase:
            raise ValueError("Password must contain uppercase")
        if not has_special_char:
            raise ValueError("Password must special character")
        
        return password


class admin_delete_user_input(BaseModel):
    username: str = Field(min_length=2, max_length=25)
    usernameconfirm: str = Field(min_length=2, max_length=25)

    @model_validator(mode="after")
    def usernames_must_match(self):
        if self.username != self.usernameconfirm:
            raise ValueError("Both usernames must match")
        return self

class dataset_input_schema(BaseModel):
    #datatset type
    dataset_type: str

    @model_validator(mode="after")
    def valid_dataset_type(self):
        titled = self.dataset_type.title()
        if titled not in ["Interactions", "Content", "Derived_Users"]:
            raise invalid_dataset_type()
        self.dataset_type = titled
        return self

    @classmethod
    def as_form(cls, dataset_type: str = Form(...)):
        return cls(dataset_type=dataset_type)


class recommendor_input_schema(BaseModel):
    algorithm_name: str


    
class store_interactions(BaseModel):
    item_id: str
    interaction_type: str
    
    @model_validator(mode="after")
    def valid_dataset_type(self):
        normalized = self.interaction_type.lower()
        if normalized not in ["like", "dislike", "report"]:
            raise ValueError("invalid interaction type")
        self.interaction_type = normalized
        return self

# NOTES
"""
- username fields (user_register_input, admin_researcher_register_Input, admin_register_input, admin_delete_user_input): need to enforce uniqueness — add a check
- password_check validators: "Password must contain uppercase" / "Password must have a special character" — convert these ValueErrors to HTTPExceptions
- admin_delete_user_input.usernames_must_match: convert ValueError to HTTPException
- dataset_input_schema.valid_dataset_type: convert to a proper HTTPException instead of raising UserNotFound() directly
- RecommendorInputSchema: commented-out validator requiring algorithm_name to start with "R" — decide whether to keep/remove/re-enable
- Ensure generated UUIDs are unique (small chance of collision — verify error handling covers this)
"""