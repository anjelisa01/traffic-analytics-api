
from sqlalchemy.orm import Session
from sqlalchemy import select


from models import Website

class WebsiteRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self, ws: Website):
        self.db.add(ws)
        self.db.commit()
        self.db.refresh(ws)
        return ws
    
    def get_by_id(self, website_id: int):
        stmt = select(Website).where(Website.id == website_id)
        return self.db.scalar(stmt)
    
    def update(self, ws: Website, update_data: dict):
        update_data = update_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(ws, field, value)

        self.db.commit()
        self.db.refresh(ws)
        return ws
    
    def delete(self, ws: Website):
        self.db.delete(ws)
        self.db.commit()