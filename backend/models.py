from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import datetime
from sqlalchemy import DateTime

class Website(Base):
    __tablename__="websites"
    #======fields
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(255))
    domain:Mapped[str]
    #======relationship
    events:Mapped[list["Event"]]=relationship(
        back_populates="website"
    )
class Event(Base):
    __tablename__="events"
    #======fields
    id:Mapped[int]=mapped_column(primary_key=True)
    event_type:Mapped[str]
    page:Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    #fk
    website_id:Mapped[int]=mapped_column(
        ForeignKey("websites.id"),
        nullable=False #mandatory
    )
    #======relationship
    website:Mapped["Website"]=relationship(
        back_populates="events"
    )