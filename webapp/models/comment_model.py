from sqlmodel import SQLModel, Field
import uuid

class Comment(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    article: uuid.UUID
    username: str
    comment_title: str
    text: str

class CreateComment(SQLModel):
    comment_title: str
    text: str

class UpdateComment(SQLModel):
    comment_title: str
    text: str