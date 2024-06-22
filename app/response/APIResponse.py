# response.py
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class APIResponse:
    @staticmethod
    def make(success: bool, data=None, message: str = None, status_code: int = 200):
        return JSONResponse(
            content={"success": success, "data": data, "message": message},
            status_code=status_code,
        )

    @staticmethod
    def success(data=None, message: str = None, status_code: int = 200):
        return APIResponse.make(success=True, data=data, message=message, status_code=status_code)

    @staticmethod
    def fail(message: str = None, status_code: int = 404):
        return APIResponse.make(success=False, message=message, status_code=status_code)