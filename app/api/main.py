from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from app.settings import settings

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
