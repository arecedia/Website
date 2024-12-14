from datetime import datetime
from email.policy import default
from time import strftime

from sqlmodel import SQLModel, Field
from dataclasses import field
import uuid

class Advertisement(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    client_name: str
    ad_title: str
    ad_content: str
    start_date: datetime
    end_date: datetime
    status: str = Field(default="active")   # "active", "paused", "completed"
    ad_type: str    # "banner", "sidebar", "popup", "native"
    target_url: str
    placement: str  # "homepage", "article_page", etc.
    impressions: int = Field(default=0)
    clicks: int = Field(default=0)
    budget: float = Field(default=0.0)
    cost_per_click: float = Field(default=0.0)
    cost_per_impression: float = Field(default=0.0)
    target_audience: str = Field(default=None)
    media_url: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, foreign_key="UpdateAdvertisement.updated_at")

class UpdateAdvertisement(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="Advertisement.id")
    client_name: str
    ad_title: str
    ad_content: str
    end_date: datetime
    status: str = Field(default="active")
    ad_type: str
    target_url: str
    placement: str  # "homepage", "article_page", etc.
    budget: float = Field(default=0.0)
    cost_per_click: float = Field(default=0.0)
    cost_per_impression: float = Field(default=0.0)
    target_audience: str = Field(default=None)
    media_url: str = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)