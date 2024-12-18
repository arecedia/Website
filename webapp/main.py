from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import uuid

from webapp import database

@asynccontextmanager
async def lifespan_function(app: FastAPI):
    database.create_db_and_tables()
    yield

def create_app():
    app = FastAPI(lifespan=lifespan_function)
    from webapp.routes import API_Routes
    from webapp.routes import Function_Routes
    from webapp.routes import View_Routes
    from webapp.auth import routes as auth_routes

    app.include_router(API_Routes.router, prefix="/api", tags=["API"])
    app.include_router(Function_Routes.router, prefix="/function", tags=["Functions"])
    app.include_router(View_Routes.router, prefix="", tags=["Display"])
    app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])

    if os.getenv("ENV") != "TEST":
        static_dir = "webapp/static"
        if os.path.exists(static_dir):
            app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
        else:
            print(f"Static Directory '{static_dir}' does not exist, skipping mounting")
            app.templates = Jinja2Templates(directory="webapp/templates")
            template_dir = "webapp/templates"
            if os.path.exists(template_dir):
                print(f"Template directory is: {template_dir}")
            else:
                print(f"Template Directory '{template_dir}' does not exist")
    return app

app = create_app()