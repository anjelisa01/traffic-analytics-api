from sqlalchemy.orm import Session
from models import Website
from website.website_schemas import WebsiteBase,WebsiteUpdate

from website.website_repositories import WebsiteRepository

class WebsiteService:
    def __init__(self,db:Session):
        self.db=db
        self.repository = WebsiteRepository(db)

    def create(self,payload:WebsiteBase):
        website = Website(
            name=payload.name,
            domain=payload.domain
        )
        try:
            website = self.repository.create(website)
        except Exception:
            self.db.rollback()
            raise
        return website
    def read_one(self,website_id):
        return self.repository.get_by_id(website_id)
    def read_many(self):
        pass
    def update(self,website_id,payload:WebsiteUpdate):
        ws = self.repository.get_by_id(website_id)
        try:
            ws = self.repository.update(ws, payload)
        except Exception:
            self.db.rollback()
            raise

        return ws
    
    def delete(self,website_id: int):
        ws = self.repository.get_by_id(website_id)
        try:
            self.repository.delete(ws)
        except Exception:
            self.db.rollback()
            raise
        return {"message": "deleted"}

        