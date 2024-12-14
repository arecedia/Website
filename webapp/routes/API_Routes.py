from dataclasses import Field
from datetime import datetime

from fastapi import FastAPI, Request,Depends, HTTPException, APIRouter
from pydantic import BaseModel, constr
from pydantic.v1 import HttpUrl
from sqlalchemy.testing.plugin.plugin_base import logging
from sqlmodel import Session, create_engine, SQLModel
from starlette.templating import Jinja2Templates

from webapp.models.Advertisement_models import Advertisement, UpdateAdvertisement
from webapp.models.user_model import User
from webapp import database
from webapp.routes.Function_Routes import create_advertisement, update_advertisement, delete_advertisement

router = APIRouter()
templates = Jinja2Templates(directory="webapp/templates")

class Advertisement(BaseModel):
    client_name: str
    ad_title: str
    ad_content: str
    start_date: datetime
    end_date: datetime
    status: str
    ad_type: str
    target_url: str
    placement: str
    media_url: str
    budget: float

class UpdateAdvertisement(BaseModel):
    client_name: str
    ad_title: str
    ad_content: str
    status: str
    end_date: datetime
    status: str
    ad_type: str
    target_url: str
    placement: str
    media_url: str


def create_advertisement(*,
                         session: Session,
                         ad_data: dict
                         ):
    return{"message":"Advertisement created successfully", "data":ad_data}


def update_advertisement(*,
                         session: Session,
                         updates: dict
                         ):
    return{"message":"Advertisement updated successfully", "updated_info": updates}

@router.post("/ads/")
async def create_ad(*,
                    ad_data: Advertisement,
                    session: Session = Depends(database.get_session),
):
    try:
        return create_advertisement(session=session, ad_data=ad_data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ads/{ad_id}")
def update_ad(*,
              ad_id: int,
              updates: UpdateAdvertisement,
              session: Session = Depends(database.get_session),
              ):
    try:
        return update_advertisement(session=session, updates=updates.dict(), ad_id=ad_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/ads/{ad_id}")
def delete_ad(*,
              ad_id: int,
              session: Session = Depends(database.get_session),
              ):
    try:
        delete_advertisement(session, ad_id)
        return {"message": "Advertisement deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))