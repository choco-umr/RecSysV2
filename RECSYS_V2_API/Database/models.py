from sqlalchemy import Column, String, Integer
from Database.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
import uuid

class Users(Base):
    __tablename__ = "Users"
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    USER_TYPE = Column("USER_TYPE", String, nullable=False)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)
    GENDER = Column("GENDER",String, nullable=False) #need to make it enum?
    AGE = Column("AGE", Integer) #add validation for between 1-100

    @validates("USER_TYPE")
    def validate_USER_TYPE(self, key, USER_TYPE):
        if USER_TYPE != "User":
            raise ValueError("Invalid user type")
        return USER_TYPE
    
    @validates("GENDER")
    def validate_USER_TYPE(self, key, GENDER):
        if GENDER not in ("Male", "Female"):
            raise ValueError("Invalid gender type")
        return GENDER


class Researchers(Base):
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    USER_TYPE = Column("USER_TYPE", String, nullable=False)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)

    @validates("USER_TYPE")
    def validate_USER_TYPE(self, key, USER_TYPE):
        if USER_TYPE != "Researcher":
            raise ValueError("Invalid user type")
        return USER_TYPE


class Admins(Base):
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    USER_TYPE = Column("USER_TYPE", String, nullable=False)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)

    @validates("USER_TYPE")
    def validate_USER_TYPE(self, key, USER_TYPE):
        if USER_TYPE != "Admin":
            raise ValueError("Invalid user type")
        return USER_TYPE



#TO/DO
#global password strength function - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
#duplicate username check function