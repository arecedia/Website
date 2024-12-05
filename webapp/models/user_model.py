from sqlmodel import SQLModel, Field
import uuid
from dataclasses import field

class User(SQLModel, table=True):
    id = uuid.uuid4 = Field(default_factory=uuid.uuid4, primary_key=True)