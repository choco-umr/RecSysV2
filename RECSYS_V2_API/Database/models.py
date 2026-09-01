import uuid

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, BigInteger, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column

from .db import Base

class Users(Base):
    __tablename__ = "Users"
    USER_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    FIRST_NAME = Column("FIRST_NAME", String, nullable=False)
    LAST_NAME = Column("LAST_NAME", String, nullable=False)
    USERNAME = Column("USERNAME", String, nullable=False)
    PASSWORD = Column("PASSWORD", String)
    GENDER = Column("GENDER",Integer, nullable=False) 
    AGE = Column("AGE", Integer)
    PREFERRED_CATEGORIES: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    PREFERRED_SUB_CATEGORIES: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    
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
    DATASET_NAME = Column(String, nullable=True)
    ITEM_ID = Column(String, nullable=False, primary_key=True)
    CATEGORY = Column(String)
    SUB_CATEGORY = Column(String)
    TITLE = Column(String, nullable=False)
    ABSTRACT = Column(String)
    TIMESTAMP = Column(DateTime)
    ARTICLE_TYPE = Column(String)

    __table_args__ = (
        UniqueConstraint(
            "DATASET_NAME", "TITLE", "CATEGORY", "SUB_CATEGORY",
            "ABSTRACT", "TIMESTAMP", "ARTICLE_TYPE",
            name="uq_content_dedup"
        ),
    )
    

class Interactions(Base):
    __tablename__ = "Interactions"
    DATASET_NAME = Column(String, nullable=False)
    INTERACTION_ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


    USER_ID = Column(String, nullable=False)
    ITEM_ID = Column(String, nullable=False)

    TIMESTAMP = Column(DateTime)
    INTERACTION_TYPE = Column(String, nullable=False)
    READ_TIME = Column(Float, nullable=True)
    SCROLL_PERCENTAGE = Column(Float, nullable=True)
    ALGORITHM_USED = Column(String, ForeignKey("RecommendorAlgorithms.ALGORITHM_NAME"), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "DATASET_NAME", "USER_ID", "ITEM_ID", "TIMESTAMP", "INTERACTION_TYPE",
            name="uq_interactions_dedup",
        ),
    )

class RecommendorAlgorithms(Base):
    __tablename__ = "RecommendorAlgorithms"
    ALGORITHM_NAME = Column(String,primary_key=True, nullable=False)
    CURRENTLY_ACTIVE = Column(Boolean, nullable=False, default=False)   
    TIMESTAMP_START = Column(DateTime)
    TIMESTAMP_END = Column(DateTime)


#NOTES
"""
GENDER: need to make it enum?
AGE: add validation for between 1-100
ITEM_ID (Content): will need to change from uuid later see user id in interactions table
INTERACTION_ID: has to be str and not uuid since items can be uploaded and they won't be uuids
USER_ID (Interactions): has to be str and not uuid since items can be uploaded and they won't be uuids
ITEM_ID (Interactions): has to be str and not uuid since items can be uploaded and they won't be uuids
ALGORITHM_USED: has to be alg name from recommender algorithms table
Database relationships need to be added
"""