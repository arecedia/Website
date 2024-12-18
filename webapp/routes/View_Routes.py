import logging
from sqlmodel import Session, select

from webapp import database
from webapp.models import user_model

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

log = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="webapp/templates")

@router.get("/", response_class=HTMLResponse)
async def home_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="homepage.html",
        context={}
    )

@router.get("/articles.html", response_class=HTMLResponse)
def articles_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="articles.html",
        context={}
    )

@router.get("/articles/{article_id}.html", response_class=HTMLResponse)
def specific_article_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/articles/{article_id}.html",
        context={}
    )

@router.get("/login.html", response_class=HTMLResponse)
def login_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@router.get("/signup.html", response_class=HTMLResponse)
def signup_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={}
    )

@router.get("/user.html", response_class=HTMLResponse)
def user_view(*,
              request: Request,
              session: Session = Depends(database.get_session)
              ):
    qry = select(user_model.User)
    users = session.exec(qry).all()

    return templates.TemplateResponse(
        request=request,
        name="user.html",
        context={"users": users}
    )