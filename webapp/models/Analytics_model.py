from sqlmodel import SQLModel, Field
import uuid

class Analytics(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    News_Title: str

class CreateAnalytics(SQLModel):
    News_Title: str

class UpdateAnalytics(SQLModel):
    News_Title: str