from fastapi import APIRouter,Depends

from event.event_schemas import EventBase, EventUpdate
from event.event_service import EventService

from dependencies import get_event_service
router=APIRouter(tags=['events'])

@router.post("/{website_id}")
def add_event(website_id:int,payload:EventBase,service:EventService=Depends(get_event_service)):
    return service.create(website_id,payload)

@router.post("/bulk/{website_id}")
def add_events(website_id:int,payload:list[EventBase],service:EventService=Depends(get_event_service)):
    return service.create_many(website_id,payload)

@router.get("/{event_id}",response_model=EventBase)
def get_event(event_id:int,service:EventService=Depends(get_event_service)):
    return service.read_one(event_id)

@router.delete("/{event_id}")
def remove_event(event_id:int,service:EventService=Depends(get_event_service)):
    return service.delete(event_id)

@router.patch("/{event_id}",response_model=EventBase)
def edit_event(event_id:int,payload:EventUpdate,service:EventService=Depends(get_event_service)):
    return service.update(event_id,payload)