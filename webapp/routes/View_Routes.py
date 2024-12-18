import logging
from sqlmodel import Session, select
from webapp import database
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from webapp.models import user_model

router = APIRouter()

log = logging.getLogger(__name__)
templates = Jinja2Templates(directory="webapp/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="homepage.html",
        context={}
    )

@router.get("/articles", response_class=HTMLResponse)
async def articles(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="articles.html",
        context={}
    )

@router.get("/articles/{article_id}", response_class=HTMLResponse)
async def specific_article(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/articles/{article_id}.html",
        context={}
    )

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )

@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse(
        request=request, name="signup.html", context={}
    )

@router.get("/user.html", response_class=HTMLResponse)
async def user_view(*,
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