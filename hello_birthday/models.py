from sqlalchemy import Column, String, Date
from .database import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True)
    dateOfBirth = Column(Date)
