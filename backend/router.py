from fastapi import APIRouter
import website.website_endpoints as website_endpoints
import event.event_endpoints as event_endpoints
import statistic.endpoint as stats_endpoints
api_router=APIRouter()

api_router.include_router(
    website_endpoints.router,
    prefix="/websites",
    tags=["websites"]
)


api_router.include_router(
    event_endpoints.router,
    prefix="/events",
    tags=["events"]
)


api_router.include_router(
    stats_endpoints.router,
    prefix="/stats",
    tags=["stats"]
)