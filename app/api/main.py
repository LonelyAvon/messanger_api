from sqlite3 import IntegrityError
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError




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

# @app.get("/GET")
# async def get(request: Request, session:AsyncSession=Depends(get_session)):
#     users = await UserRepository(session).get_all()
#     return users

# @app.put("/update", response_model=UserRead)
# async def put(request: Request, user: UserUpdate, session:AsyncSession=Depends(get_session)):
#     user = await UserRepository(session).update_one(user)
#     await UserRepository(session).commit()
#     return user

