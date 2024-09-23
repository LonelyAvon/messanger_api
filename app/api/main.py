from sqlite3 import IntegrityError
from fastapi import Depends, FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.api.schemas.user import UserRead
from app.api.schemas.sales_returns import SalesReturnsDay
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from .authorization.func import get_current_user



app = FastAPI(
    title=settings.PROJECT_TITLE, 
    version="1.0.0",
    root_path=settings.FAST_API_PREFIX
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

@app.get("/users/me", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user

@app.post("/sales_returns/graph", response_model=list[SalesReturnsDay])
async def sales_returns_graph():
    pass