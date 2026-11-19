from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date, timedelta
from fastapi import FastAPI, Query, Depends
from models import Event,Website
from dependencies import get_db
from typing import Literal

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

#statistic summary
from pagination import pagination
@router.get("/data")
def get_data(    #get data with all filters
    website_id:int | None = Query(default=None),
    event_type:str | None = Query(default=None),
    page:str | None = Query(default=None),
    timestamp: date | None = Query(default=None),
    sort_by: Literal["page", "event","timestamp"] = Query(default="page"), #, "total_event"
    order: Literal["asc", "desc"] = Query(default="asc"),
    paging: dict = Depends(pagination),

    db: Session = Depends(get_db)):

    stmt=select(Event)

    if website_id is not None:
        stmt=stmt.where(Event.website_id==website_id)
    if event_type is not None:
        stmt=stmt.where(Event.event_type==event_type)
    if timestamp is not None:
        stmt = stmt.where(
            Event.timestamp >= timestamp,
            Event.timestamp < timestamp + timedelta(days=1)
        )

    if page is not None:
        stmt=stmt.where(Event.page==page)

    sort_columns = {
        "page": Event.page,
        "event": Event.event_type,
        "timestamp":Event.timestamp
        }
    sort_column = sort_columns[sort_by]

    stmt = stmt.order_by(
        sort_column.desc() if order == "desc" else sort_column.asc()
    )
    stmt =stmt.offset(paging['skip']).limit(paging['limit'])

    results = db.execute(stmt).scalars().all()    #print(type(results[0]))
    print(results[0])
    print(Event.__table__.columns.keys())
    return [
        {
        "id": event.id,
        "website_id": event.website_id,
        "timestamp": event.timestamp,
        "page": event.page,
        "event_type": event.event_type
    }
    for event in results
    ]


#dashboard endpoint.
#users data in a glance
@router.get("/total")
def get_summary(
    timestamp: date | None = Query(default=None),
    sort_by: Literal["page", "event","total_event"] = Query(default="total_event"), 
    order: Literal["asc", "desc"] = Query(default="asc"),
    paging: dict = Depends(pagination),
    db: Session = Depends(get_db)):
    stmt=select(
            Event.event_type,
            Event.page,
            Event.website_id,
            Website.name.label("website_name"),
            func.count(Event.id).label("total_events") #add website_id. add filter by timestamp, add order by
        ).join(
            Website,
            Event.website_id == Website.id
        )
    if timestamp is not None:
            stmt = stmt.where(
                Event.timestamp >= timestamp,
                Event.timestamp < timestamp + timedelta(days=1)
            )

    stmt=stmt.group_by(Event.page, Event.event_type,Event.website_id,Website.name)
    stmt=stmt.order_by(
        Event.website_id.asc(),
        Event.page.asc(),
        func.count(Event.id).desc()
    ) #make dynamic, by id still static by default asc, page and count is dynamic
    
    results= db.execute(stmt).all()
        
    data = {}

    for row in results:
        if row.website_id not in data:
            data[row.website_id] = {
                "website_id": row.website_id,
                "website_name":row.website_name,
                "timestamp": timestamp.isoformat() if timestamp else None,
                "events_counts": {}
            }
        if row.page not in data[row.website_id]["events_counts"]:
            data[row.website_id]["events_counts"][row.page] = {}

        data[row.website_id]["events_counts"][row.page][row.event_type] = row.total_events
    # for row in results:
    #     if row.page not in data:
    #         data[row.page] = {}
    #     data[row.page][row.event_type] = row.total_events
    return data


'''
note on aggregation.

use groupby to use aggregate function to different groups
so aggregation function can be use alone but it will apply to entire table


SELECT
    page,           #this thirs, so after applying the count, we want to return the page value
    COUNT(id)       #this second, so in those groups created we apply count(id) which count how many id
                    #so because this in SELECT  meaning it will be return as a column
                    #each column:page and count(id) can be missing (well not both at the same time), but we use it so we know the pages and their counts
FROM events
GROUP BY page;      #this first, so sql group data in table events by page


ORDER
Remember the order
SQL clause	Purpose
FROM	Get the events table.
WHERE	Filter which rows you want.         #USE WHERE TO FILTER so the data left is the one going to be use in the calculation, USE HAVING TO FILTER AFTER AGGREGATION like a further analysis
GROUP BY	Group the remaining rows.       
COUNT()	Count rows in each group.
SELECT	Return the requested columns and counts.
'''








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

