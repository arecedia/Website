import logging
from typing import Annotated, Optional
from pydantic import BaseModel
import jwt
from sqlmodel import Session, select
from optparse import Values
from datetime import datetime
from sqlmodel import Session

from webapp.models import user_model, Article_model, Analytics_model, Advertisement_models, Interaction_model, comment_model
from webapp import database
from webapp.auth import service as auth_service
from webapp.auth import routes as auth_routes

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

log = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="webapp/templates")

@router.get("/login.html", response_class=JSONResponse)
async def login_code(
                request: Request,
                session: Session = Depends(database.get_session),
):
    """
    Handle user login, verify credentials, and return an access token
    """

    body = await request.json()
    email = body.get("email/username")
    username = body.get("email/username")
    password = body.get("password")

    qry = select(user_model.User).where(user_model.User.email == email)
    result1 = session.exec(qry).first()
    if result1:
        # Check if the entered detail is an email or a username
        isEmail = True

    qry = select(user_model.User).where(user_model.User.username == username)
    result2 = session.exec(qry).first()
    if result2:
        isUsername = True

    if isEmail == True:
        # Check if the password is correct
        if result1.verify_password(password):
            # Create an Access token
            if result1.admin == False:
                encoded_jwt = auth_service.create_access_token(
                    data={"audience": "User",
                          "subject": result1.id.hex}
                )
            else:
                encoded_jwt = auth_service.create_access_token(
                    data={"audience": "Admin",
                          "subject": result1.id.hex}
                )
            response = JSONResponse(
                content={"success": True,
                        "redirect_url": "http://127.0.0.1:8000"}
            )
            response.set_cookie(key="access_token", value=encoded_jwt)
        else:
            return JSONResponse(content={"success": False, "message": "Invalid email or password"})
    elif isUsername == True:
        # Check if the password is correct
        if result2.verify_password(password):
            # Create an Access token
            if result2.admin == False:
                encoded_jwt = auth_service.create_access_token(
                    data={"audience": "User",
                          "subject": result2.id.hex}
                )
            else:
                encoded_jwt = auth_service.create_access_token(
                    data={"audience": "Admin",
                          "subject": result2.id.hex}
                )
            response = JSONResponse(
                content={"success": True,
                         "redirect_url": "http://127.0.0.1:8000"}
            )
            response.set_cookie(key="access_token", value=encoded_jwt)
        else:
            return JSONResponse(content={"success": False, "message": "Invalid username or password"})
    else:
        print("No User Found")
    if isEmail:
        admin = result1.admin
        if admin == True:
            encoded_jwt = auth_service.create_access_token(email=email, data={"audience": "Admin", "subject": result1.id.hex})
        elif admin == False:
            encoded_jwt = auth_service.create_access_token(email=email, data={"audience": "User", "subject": result1.id.hex})
    if isUsername:
        admin = result2.admin
        if admin == True:
            encoded_jwt = auth_service.create_access_token(email=email, data={"audience": "Admin", "subject": result2.id.hex})
        elif admin == False:
            encoded_jwt = auth_service.create_access_token(email=email, data={"audience": "User", "subject": result2.id.hex})

    response = JSONResponse(content={"success": True, "message": "Login Successful", "redirect_url": "http://127.0.0.1:8000"})
    response.set_cookie(key="access_token", value=encoded_jwt)

    return response

@router.get("/signup.html", response_class=JSONResponse)
async def signup_code(*,
                      request: Request,
                      session: Session = Depends(database.get_session)
                      ):
    """
    Handle User signup, verifying details are not already taken, and returns an access token
    """

    body = await request.json()
    username = body.get("username")
    email = body.get("email")
    password = body.get("password")
    cPassword = body.get("cPassword")

    qry = select(user_model.User).where(user_model.User.email == email)
    result = session.exec(qry).first()
    qry = select(user_model.User).where(user_model.User.username == username)
    result2 = session.exec(qry).first()

    if result or result2:
        return JSONResponse(content={"success": False, "message": "Invalid User Credentials"})

    else:
        if password != cPassword:
            return JSONResponse(content={"success": False, "message": "Invalid User Credentials"})
        else:
            db_user = user_model.User(email=email, username=username, admin=False)
            db_user.update_password(password)
            session.add(db_user)

            session.commit()
            encoded_jwt = auth_service.create_access_token(email=email, data={"audience": "User", "subject": result.id.hex})
            response = JSONResponse(content={"success": True, "message": "User Created"})
    response.set_cookie(key="access_token", value=encoded_jwt)
    return response

@router.get("/articles/comment.html", response_class=JSONResponse)
async def comment_code(*,
                       request: Request,
                       session: Session = Depends(database.get_session),
                       user_details: user_model.User = Depends(auth_service.get_auth_user),
                       ):
    body = await request.json()
    commentTarget = body.get("Target")
    commentTitle = body.get("Title")
    commentText = body.get("Text")
    username = user_details.username

    qry = select(user_model.User).where(user_model.User.username == username)
    result2 = session.exec(qry).first()
    if result2:
        response = JSONResponse(
            content={"success": True, "redirect_url": "http://127.0.0.1:8000/articles/{article_id}"}
        )

        db_info = (comment_model.Comment(
            article=commentTarget,
            comment_title=commentTitle,
            text=commentText,
            username=username))

        session.add(db_info)
        session.commit()
        return response
    else:
        response = JSONResponse(
            content={"success": False, "message": "Invalid cookie detected"}
        )
        return response
