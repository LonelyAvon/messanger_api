from sqlite3 import IntegrityError
from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.api.schemas.user import UserRead
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from .authorization.func import get_current_user



app = FastAPI(
    title=settings.fast_api_title, 
    version="1.0.0",
    root_path=settings.fast_api_prefix
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    raise HTTPException(status_code=400, detail=str(exc.orig).split("\nDETAIL:  ")[1])


app.include_router(api_router)

@app.get("/GET", response_model=UserRead)
async def get(request: Request, user: UserRead = Depends(get_current_user)):
    return user