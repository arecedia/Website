from sqlmodel import SQLModel, Field
import uuid
from typing import Optional
from dataclasses import field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    created_ad: Optional[str] = Field(default=None)