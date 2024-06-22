from fastapi import FastAPI,Request
import uvicorn
from routers.api.v1.auth import auth_router
from routers.web import web_router
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    title="FastAPIs",
    description="Having request methods",
    version="1.0.0"
)

app.add_middleware(SessionMiddleware, secret_key="some-random-string")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{err["loc"][1]: err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"errors": errors},
    )
    
app.include_router(web_router)
app.include_router(auth_router)

if __name__=="__main__":
    uvicorn.run("app.api:app", host=os.getenv('APP_HOST'), port=os.getenv('APP_PORT'), reload=True)