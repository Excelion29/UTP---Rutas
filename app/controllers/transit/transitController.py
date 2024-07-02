
from app.response.APIResponse import APIResponse
from fastapi import HTTPException
import httpx
import os

async def get_routes(start_lat,start_lng,end_lat,end_lng):
    try:
        url = os.getenv('TRANSIT_URL') + "/api/v2/routing/otp/plan"
        api_key = os.getenv("TRANSIT_API_KEY")
        params = {
            "fromPlace":(start_lat,start_lng),
            "toPlace": (end_lat,end_lng),
            "api_key": api_key,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Verifica si hay errores HTTP
            data = response.json()
            return APIResponse.success(data, "Ruta obtenida exitosamente")
    except httpx.HTTPStatusError as e:
        return APIResponse.fail(f"HTTP error: {e}", status_code=e.response.status_code) 
    except httpx.RequestError as e:
        return APIResponse.fail(f"Request error: {e}")
    except HTTPException as e:
        return APIResponse.fail(str(e.detail), status_code=e.status_code)