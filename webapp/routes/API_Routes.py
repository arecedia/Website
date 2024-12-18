from dataclasses import Field
from datetime import datetime
import uuid

from fastapi import FastAPI, Request,Depends, HTTPException, APIRouter
from pydantic import BaseModel, constr
from pydantic.v1 import HttpUrl
from sqlalchemy.testing.plugin.plugin_base import logging
from sqlmodel import Session, create_engine, SQLModel
from starlette.templating import Jinja2Templates

from webapp.models.Advertisement_models import Advertisement, CreateAdvertisement, UpdateAdvertisement
from webapp.models.Analytics_model import Analytics, CreateAnalytics, UpdateAnalytics
from webapp.models.Article_model import  Article, CreateArticle, UpdateArticle
from webapp.models.comment_model import Comment, CreateComment, UpdateComment
from webapp.models.Interaction_model import Interaction, CreateInteraction, UpdateInteraction
from webapp.models.user_model import User, CreateUser, UserUpdate

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

    return{"message": "Advertisement created successfully", "data": new_ad}


@router.put("/ads/{id}")
def update_ad(*,
              id: int,
              updates: UpdateAdvertisement,
              session: Session = Depends(database.get_session),
              ):
    try:
        advertisement = session.get(Advertisement, id)
        if not advertisement:
            raise HTTPException(status_code=404, detail="Advertisement not found")

        for key, value in updates.dict(exclude_unset=True).items():
            setattr(advertisement, key, value)

        advertisement.updated_at = datetime.utcnow()
        session.add(advertisement)
        session.commit()
        session.refresh(advertisement)

        return {"message": "Advertisement updated successfully", "updated_info": advertisement}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/ads/{id}")
def delete_ad(*,
              id: int,
              session: Session = Depends(database.get_session),
              ):
    try:
        delete_advertisement(session, id)
        return {"message": "Advertisement deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/user/", response_model=CreateUser)
def create_user(*,
                user_data: CreateUser,
                session: Session = Depends(database.get_session)
                ):
    # Create a new User instance
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password = user_data.password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return{"message": "User created successfully", "data": new_user}

@router.put("/user/{id}")
def update_user(*,
                id: uuid.uuid4,
                updates: UserUpdate,
                session: Session = Depends(database.get_session)
                ):
    try:
        user = session.get(Advertisement, id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(user, key, value)

        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "User updated successfully", "updated_info": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/user/{id}")
def delete_user(*,
                id: int,
                session: Session = Depends(database.get_session),
                ):
    try:
        delete_user(session, id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/interaction/")
def create_interaction(*,
                       interaction_data: CreateInteraction,
                       session: Session = Depends(database.get_session)
                       ):
    # Create a new interaction instance
    new_interaction = Interaction(
        like = interaction_data.like,
        dislike = interaction_data.dislike,
        comments = interaction_data.comments
    )

    session.add(new_interaction)
    session.commit()
    session.refresh(new_interaction)

    return{"message": "Interaction created successfully", "data": new_interaction}

@router.put("/interaction/{id}")
def update_interaction(*,
                id: int,
                updates: UpdateInteraction,
                session: Session = Depends(database.get_session)
                ):
    try:
        interaction = session.get(Interaction, id)
        if not interaction:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(interaction, key, value)

        session.add(interaction)
        session.commit()
        session.refresh(interaction)

        return {"message": "Interaction updated successfully", "updated_info": interaction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/interaction/{id}")
def delete_interaction(*,
                id: int,
                session: Session = Depends(database.get_session),
                ):
    try:
        delete_interaction(session, id)
        return {"message": "Interaction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/comment/")
def create_comment(*,
                       comment_data: CreateComment,
                       session: Session = Depends(database.get_session)
                       ):
    # Create a new interaction instance
    new_comment = Comment(
        comment_title = comment_data.comment_title,
        username = comment_data.username,
        text = comment_data.text,
    )

    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)

    return{"message": "Interaction created successfully", "data": new_comment}

@router.put("/comment/{id}")
def update_comment(*,
                       id: int,
                       comment: UpdateComment,
                       session: Session = Depends(database.get_session)
                       ):
    try:
        comment = session.get(Comment, id)
        if not comment:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in comment.dict(exclude_unset=True).items():
            setattr(comment, key, value)

        session.add(comment)
        session.commit()
        session.refresh(comment)

        return {"message": "Comment updated successfully", "updated_info": comment}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/comment/{id}")
def delete_comment(*,
                       id: int,
                       session: Session = Depends(database.get_session),
                       ):
    try:
        delete_comment(session, id)
        return {"message": "Comment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/Article/")
def create_article(*,
                       article_data: CreateArticle,
                       session: Session = Depends(database.get_session)
                       ):
    # Create a new interaction instance
    new_article = Article(
        article_id = article_data.article_id,
        headline = article_data.headline,
        image_URL = article_data.image_URL,
    )

    session.add(new_article)
    session.commit()
    session.refresh(new_article)

    return{"message": "Article created successfully", "data": new_article}

@router.put("/article/{id}")
def update_article(*,
                       id: int,
                       updates: UpdateArticle,
                       session: Session = Depends(database.get_session)
                       ):
    try:
        article = session.get(Article, id)
        if not article:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(article, key, value)

        session.add(article)
        session.commit()
        session.refresh(article)

        return {"message": "Article updated successfully", "updated_info": article}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/article/{id}")
def delete_article(*,
                       id: int,
                       session: Session = Depends(database.get_session),
                       ):
    try:
        delete_article(session, id)
        return {"message": "Article deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))