from typing import Union
from pydantic import BaseModel

# class UserBase(BaseModel):
#     username: str

class UserDOB(BaseModel):
    dateOfBirth: str

class Message(BaseModel):
    message: str