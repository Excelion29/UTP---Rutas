from fastapi import APIRouter,HTTPException,Query
from fastapi.security import HTTPBearer
from app.controllers.transit.transitController import get_routes

transit_router = APIRouter(prefix="/api/v1/transit", tags=["transit"])
bearer = HTTPBearer()

@transit_router.get("/get_routes")
async def get_transit_routes(
        start_lat: float = Query(..., description="Starting latitude", ge=-90, le=90),
        start_lng: float = Query(..., description="Starting longitude", ge=-180, le=180),
        end_lat: float = Query(..., description="Ending latitude", ge=-90, le=90),
        end_lng: float = Query(..., description="Ending longitude", ge=-180, le=180)
    ):
    try:
        response = await get_routes(start_lat,start_lng,end_lat,end_lng)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")