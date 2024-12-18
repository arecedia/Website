from sqlmodel import SQLModel, Field
import uuid
from webapp.models.Interaction_model import Interaction

class Article(SQLModel, table=True):
    article_id: int = Field(primary_key=True)
    headline: str
    image_URL: str
    visible: bool
    likes: int = Field(foreign_key="Interaction.likes")
    dislikes: int = Field(foreign_key="Interaction.dislikes")
    comments: int = Field(foreign_key="Interaction.comments")

class CreateArticle(SQLModel):
    headline: str
    image_URL: str
    visible: bool = Field(default=False)
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    comments: int = Field(default=0)

class UpdateArticle(SQLModel):
    Article_Title: str | None = None
    image_url: str | None = None
    visible: bool | None = None

