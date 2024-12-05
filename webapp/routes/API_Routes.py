from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.testing.plugin.plugin_base import logging
from sqlmodel import Session, create_engine, SQLModel
from starlette.templating import Jinja2Templates

from webapp.models.Advertisement_models import Advertisement
from webapp.models.user_model import User
from webapp import database
from webapp.routes.Function_Routes import create_advertisement, update_advertisement, delete_advertisement

log = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="webapp/templates")

@router.post("/ads/")
def create_ad(*,
              ad_data: dict,
              session: Session = Depends(database.get_session),
              ):
    try:
        return create_advertisement(session, ad_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/ads/{ad_id}")
def update_ad(*,
              ad_id: int,
              updates: dict,
              session: Session = Depends(database.get_session),
              ):
    try:
        return update_advertisement(session, ad_id, updates)
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