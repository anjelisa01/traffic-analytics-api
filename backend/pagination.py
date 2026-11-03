
from fastapi import Query

def pagination(
    skip: int = Query(0, ge=0), #this create query parameter
    limit: int = Query(10, ge=1, le=100)
):
    return {
        "skip": skip,
        "limit": limit
    }
