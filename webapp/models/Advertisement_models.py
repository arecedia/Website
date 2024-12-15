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
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CreateAdvertisement(SQLModel):
    client_name: str
    ad_title: str
    ad_content: str
    start_date: datetime
    end_date: datetime
    status: str
    ad_type: str
    target_url: str
    placement: str
    budget: float
    cost_per_click: float
    cost_per_impression: float
    target_audience: str
    media_url: str
    created_at: datetime



class UpdateAdvertisement(SQLModel):
    client_name: str
    ad_title: str
    ad_content: str
    end_date: datetime
    status: str
    ad_type: str
    target_url: str
    placement: str  # "homepage", "article_page", etc.
    budget: float
    cost_per_click: float
    cost_per_impression: float
    target_audience: str
    media_url: str