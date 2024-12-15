from dataclasses import Field
from datetime import datetime

from fastapi import FastAPI, Request,Depends, HTTPException, APIRouter
from pydantic import BaseModel, constr
from pydantic.v1 import HttpUrl
from sqlalchemy.testing.plugin.plugin_base import logging
from sqlmodel import Session, create_engine, SQLModel
from starlette.templating import Jinja2Templates

from webapp.models.Advertisement_models import Advertisement, CreateAdvertisement, UpdateAdvertisement
from webapp.models import Analytics_model
from webapp.models import Article_model
from webapp.models import comment_model
from webapp.models import Interaction_model
from webapp.models import user_model

from webapp import database
from webapp.routes.Function_Routes import create_advertisement, update_advertisement, delete_advertisement

router = APIRouter()
templates = Jinja2Templates(directory="webapp/templates")


@router.post("/ads/", response_model=CreateAdvertisement)
def create_ad(*,
              ad_data: CreateAdvertisement,
              session: Session = Depends(database.get_session)):
    # Validate date range
    if ad_data.start_date >= ad_data.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before the end date.")

    # Create a new Advertisement instance
    new_ad = Advertisement(
        client_name=ad_data.client_name,
        ad_title=ad_data.ad_title,
        ad_content=ad_data.ad_content,
        start_date=ad_data.start_date,
        end_date=ad_data.end_date,
        status=ad_data.status,
        ad_type=ad_data.ad_type,
        target_url=ad_data.target_url,
        placement=ad_data.placement,
        budget=ad_data.budget,
        cost_per_click=ad_data.cost_per_click,
        cost_per_impression=ad_data.cost_per_impression,
        target_audience=ad_data.target_audience,
        media_url=ad_data.media_url,
        created_at=ad_data.created_at,
    )

    # Add and commit the new advertisement
    session.add(new_ad)
    session.commit()
    session.refresh(new_ad)

    return{"message": "Advertisement created successfully", "data":new_ad}


@router.put("/ads/{ad_id}")
def update_ad(*,
              ad_id: int,
              updates: UpdateAdvertisement,
              session: Session = Depends(database.get_session),
              ):
    try:
        advertisement = session.get(Advertisement, ad_id)
        if not advertisement:
            raise HTTPException(status_code=404, detaul="Advertisement not found")

        for key, value in updates.dict(exclude_unset=True).items():
            setattr(advertisement, key, value)

        advertisement.updated_at = datetime.utcnow()
        session.add(advertisement)
        session.commit()
        session.refresh(advertisement)

        return {"message": "Advertisement updated successfully", "updated_info": advertisement}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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