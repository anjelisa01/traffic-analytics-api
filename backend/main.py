from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import Base
from database import engine

from router import api_router

Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(api_router, prefix="/api")