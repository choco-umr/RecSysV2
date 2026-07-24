from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, BigInteger
from Database.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates, relationship
import uuid

class Users(Base):
    __tablename__ = "Users"
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)
    GENDER = Column("GENDER",Integer, nullable=False) #need to make it enum?
    AGE = Column("AGE", Integer) #add validation for between 1-100
    
    @validates("GENDER")
    def validate_GENDER(self, key, GENDER):
        if GENDER not in (1, 2):
            raise ValueError("Invalid gender type")
        return GENDER

class Researchers(Base):
    __tablename__ = "Researchers"
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)

class Admins(Base):
    __tablename__ = "Admins"
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)

class Content(Base):
    __tablename__ = "Content"
    ITEM_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    DATASET_NAME = Column(String, nullable=True)
    TITLE = Column(String, nullable=False)
    CATEGORY = Column(String)
    SUBCATEGORY = Column(String)
    ABSTRACT = Column(String)
    TIME_PUBLISHED = Column(DateTime)
    ARTICLE_TYPE = Column(String)
 
class Dataset_Upload_Tracking(Base):
    __tablename__ = "Dataset_Upload_Tracking"

    UPLOAD_ID = Column(UUID)
    FILENAME = Column(String)
    DATASET_TYPE = Column(String)
    UPLOADED_BY_USER_ID = Column(UUID)
    UPLOADED_AT = Column(DateTime(timezone=True))
    FILE_SIZE = Column(BigInteger) #FIX THIS
    ROW_COUNT = Column(Integer, nullable=True) # how are we going to get this
    UPLOAD_STATUS = Column(String)  # Uploaded or Failed

    # we already validate dataset type in schema and we validate fiel extension and file size in security



class Interactions(Base):
    __tablename__ = "Interactions"
    INTERACTION_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Removed FK relationships for now - researchers can upload interaction
    # datasets from external sources, and those datasets reference users and
    # content items that don't exist in our own Users/Content tables (discuss wiht tom about derived users coming). A hard
    # FK constraint would reject those inserts outright, since Postgres
    # requires the referenced row to exist. Left as plain UUID columns until
    # we decide on the right long-term approach (likely separate real-FK vs
    # external-reference columns, gated by DATASET_NAME).
    USER_ID = Column(UUID(as_uuid=True), nullable=False)
    ITEM_ID = Column(UUID(as_uuid=True), nullable=False)

    DATETIME = Column(DateTime)
    INTERACTION_TYPE = Column(String, nullable=False)
    READ_TIME = Column(Float)
    SCROLL_PERCENTAGE = Column(Float)

#TO/DO
#global password strength function - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html