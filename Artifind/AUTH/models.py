#here we create the tables we need in our database
from msilib import Table
from click import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

 

Base = declarative_base()

class BaseUser(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    nom = Column(String(length=50))
    prenom = Column(String(length=50))
    hashed_password = Column(String(length=255))
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(length=50))

class Admin(BaseUser):
    __tablename__ = "admins"

class users(BaseUser):
    __tablename__ = "Users"

class Moderator(BaseUser):
    __tablename__ = "moderators"
