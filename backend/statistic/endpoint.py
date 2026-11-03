from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date, timedelta
from fastapi import FastAPI, Query, Depends
from models import Event,Website
from dependencies import get_db

router=APIRouter(tags=['stats'])

'''
statistic:
as a website owner i would like to know:
1. how many events per page
2. how many events per page in a certain date/time
3. how many events happens for a website in a certain date/time
4. i want to compare event_type per page in a certain time/date

detail for no4:
    a website
        /about
            event 1: total_event
            event 2: total_event
            event 3: total_event
        /product
            event 1: total_event
            event 2: total_event
            event 3: total_event            

/{website_id}  website_id mandatory
param(
    website_id:int,
    event_type:str default all
    page:str default all
    timestamp:date default none
)
'''
from typing import Literal

@router.get("/events/{website_id}")
def get_events_detail_by_page(
    website_id:int,
    timestamp: date | None = Query(default=None),
    sort_by: Literal["page", "event", "total_event"] = Query(default="page"),
    order: Literal["asc", "desc"] = Query(default="asc"),
    db: Session = Depends(get_db)):
    stmt=(
        select(
            Event.page,
            Event.event_type,
            func.count(Event.id).label("total_events")
            ).where(
            Event.website_id==website_id,
            *(
                [
                    Event.timestamp >= timestamp,
                    Event.timestamp < timestamp + timedelta(days=1)
                ] if timestamp is not None else []
            )
        ).group_by(Event.page,
                   Event.event_type)  #.order_by(Event.page)
    ) 
    sort_columns = {
        "page": Event.page,
        "event": Event.event_type,
        "total_event": func.count(Event.id)
    }

    sort_column = sort_columns[sort_by]
    stmt = stmt.order_by(
        sort_column.desc() if order == "desc" else sort_column.asc()
    )


    results= db.execute(stmt).all()
    return [
        {
            "page": row.page,
            "event": row.event_type,
            "total_event": row.total_events
        }
        for row in results
    ]

@router.get("/pages/{website_id}")
def get_total_events_by_page(
    website_id:int,
    timestamp: date | None = Query(default=None),
    db: Session = Depends(get_db)):
   
    stmt=(
        select(
            Event.page,
            func.count(Event.id).label("total_events")
            ).where(
            Event.website_id==website_id,
            *(
                [
                    Event.timestamp >= timestamp,
                    Event.timestamp < timestamp + timedelta(days=1)
                ] if timestamp is not None else []
            )
        ).group_by(Event.page)
    )  
    results= db.execute(stmt).all()
    return [
        {
            "page": row.page,
            "total_event": row.total_events
        }
        for row in results
    ]


from pagination import pagination
@router.get("/{website_id}")
def get_all_data(
    website_id:int,
    page: dict = Depends(pagination),
    db: Session = Depends(get_db)):
    stmt=(
        select(Event)
        .where(Event.website_id==website_id)
        .order_by(Event.id)
        .offset(page['skip'])
        .limit(page['limit'])
    )
    
    results= db.scalars(stmt).all()
    return results






@router.get("/")
def total_events(db: Session = Depends(get_db)):
    stmt=(
        select(
            Event.page,
            func.count(Event.id).label("total_event")         
        )
        .group_by(Event.page)
    )
    results= db.execute(stmt).all()
    return [
        {
            "page": row.page,
            "total_event": row.total_event
        }
        for row in results
    ]

