from sqlalchemy.orm import Session
from sqlalchemy import select

from models import Event

class EventRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self, e: Event):
        self.db.add(e)
        self.db.commit()
        self.db.refresh(e)
        return e
    def create_many(self, events: list[Event]):
        self.db.add_all(events)
        self.db.commit()

        for event in events:
            self.db.refresh(event)

        return events
    def get_by_id(self, event_id: int):
        stmt = select(Event).where(Event.id == event_id)
        return self.db.scalar(stmt)
    
    def update(self, e: Event, update_data: dict):
        update_data = update_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(e, field, value)

        self.db.commit()
        self.db.refresh(e)
        return e
    
    def delete(self, e: Event):
        self.db.delete(e)
        self.db.commit()    