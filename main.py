from admin import setup_admin

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.base_model import db
from routers import router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await db.create_all()
    print("project ishga tushdi")
    yield
    print("project toxtadi")


app = FastAPI(docs_url="/", lifespan=lifespan)
app.include_router(router, prefix="/api/v1")

setup_admin(app, db._engine)
