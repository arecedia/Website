from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from fastapi import Response, Depends, APIRouter, HTTPException
from sqlmodel import Session

from webapp.auth import service as auth_service
from webapp import database

router = APIRouter()

@router.post("/token")
async def get_token(*,
                    response: Response,
                    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                    session: Session = Depends(database.get_session),
                    status):
    '''
    Conform to OAuth2 Spec, around login forms though a token url
    '''

    username = form_data.username  # Part of the spec
    password = form_data.password

    # Get a User, and the Token from the validate_token function
    valid_login = auth_service.validate_login(username, password, session)
    if not valid_login:
        raise HTTPException(401, detail="Invalid User or Password")

    status, token = valid_login
    return {"access_token": token, "token_type": "bearer"}


@router.post("/Cookie")
async def get_cookie(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(database.get_session),
):
    """
    Conform to OAuth2 Spec, around login forms though a token url.
    But return a Cookie as well as a token
    """
    username = form_data.username  # Part of the spec
    password = form_data.password

    # Get a User, and the Token from the validate_token function
    valid_login = auth_service.validate_login(username, password, session)
    if not valid_login:
        raise HTTPException(401, detail="Invalid User or Password")

    status, token = valid_login

    # Set a Cookie Value here.
    response.set_cookie(key="access_token", value=token)
    return {"access_token": token, "token_type": "bearer"}