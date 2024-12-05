import logging
from optparse import Values
from datetime import datetime
from sqlmodel import Session

from webapp.models.Advertisement_models import Advertisement
from webapp import database

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm


def create_advertisement(*,
                         session: Session,
                         ad_data: dict) -> Advertisement:
    new_ad = Advertisement(**ad_data)
    session.add(new_ad)
    session.commit()
    session.refresh(new_ad)
    return new_ad


def update_advertisement(session: Session, ad_id: int, updates: dict) -> Advertisement:
    ad = session.get(Advertisement, ad_id)
    if not ad:
        raise ValueError(f"Advertisement with id {ad_id} not found.")

    for key, value in updates.items():
        setattr(ad, key, value)

    ad.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(ad)
    return ad


def delete_advertisement(session: Session, ad_id: int) -> None:
    ad = session.get(Advertisement, ad_id)
    if not ad:
        raise ValueError(f"Advertisement with id {ad_id} not found.")

    session.delete(ad)
    session.commit()


def get_advertisement_by_id(session: Session, ad_id: int) -> Advertisement:
    ad = session.get(Advertisement, ad_id)
    if not ad:
        raise ValueError(f"Advertisement with id {ad_id} not found")
    return ad


def get_all_advertisements(session: Session) -> list[Advertisement]:
    return session.query(Advertisement).all()


