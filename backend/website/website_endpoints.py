from fastapi import APIRouter,Depends

from dependencies import get_website_service
from website.website_schemas import WebsiteBase,WebsiteUpdate
from website.website_service import WebsiteService
router=APIRouter(tags=['websites'])

@router.post("/",response_model=WebsiteBase)
def add_website(payload:WebsiteBase,service:WebsiteService=Depends(get_website_service)):
    return service.create(payload)

@router.get("/{website_id}",response_model=WebsiteBase)
def get_website(website_id:int,service:WebsiteService=Depends(get_website_service)):
    return service.read_one(website_id)

@router.get("/")
def get_websites():
    return "hell"

@router.delete("/{website_id}")
def remove_website(website_id:int,service:WebsiteService=Depends(get_website_service)):
    return service.delete(website_id)

@router.patch("/{website_id}",response_model=WebsiteBase)
def edit_website(website_id:int,payload:WebsiteUpdate,service:WebsiteService=Depends(get_website_service)):
    return service.update(website_id,payload)