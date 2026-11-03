from sqlalchemy.orm import Session
from models import Event
from event.event_schemas import EventBase,EventUpdate


from event.event_repositories import EventRepository

class EventService:
    def __init__(self,db:Session):
        self.db=db
        self.repository = EventRepository(db)

    def create(self,website_id:int,payload:EventBase):
        event = Event(
            event_type=payload.event_type,
            page=payload.page,
            timestamp=payload.timestamp,
            website_id=website_id #assign value for the website_id field
        )
        try:
            event = self.repository.create(event)
        except Exception:
            self.db.rollback()
            raise
        return event
    
    def create_many(self, website_id: int, payload: list[EventBase]):
        events = [
            Event(
                event_type=item.event_type,
                page=item.page,
                website_id=website_id,
                timestamp=item.timestamp,
            )
            for item in payload
        ]

        try:
            created_events = self.repository.create_many(events)
        except Exception:
            self.db.rollback()
            raise

        return created_events
    
    def read_one(self,event_id:int):
        return self.repository.get_by_id(event_id)
   
    # def read_many(self):
    #     pass

    def update(self,event_id,payload:EventUpdate):
        e = self.repository.get_by_id(event_id)
        try:
            e = self.repository.update(e, payload)
        except Exception:
            self.db.rollback()
            raise

        return e
    
    def delete(self,event_id: int):
        e = self.repository.get_by_id(event_id)
        try:
            self.repository.delete(e)
        except Exception:
            self.db.rollback()
            raise
        return {"message": "deleted"}

