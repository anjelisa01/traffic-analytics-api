from database import SessionLocal

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()


#===========

from fastapi import Depends
from sqlalchemy.orm import Session

from website.website_service import WebsiteService
from event.event_service import EventService
# from dependencies import get_db

def get_website_service(db: Session = Depends(get_db)):
    return WebsiteService(db)


def get_event_service(db: Session = Depends(get_db)):
    return EventService(db)