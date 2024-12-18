from sqlmodel import SQLModel, Field
import uuid

class Interaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    Article_Title: str
    like: int
    dislike: int
    comments: int

class CreateInteraction(SQLModel):
    like: int
    dislike: int
    comments: int

class UpdateInteraction(SQLModel):
    like: int
    dislike: int
    comments: int