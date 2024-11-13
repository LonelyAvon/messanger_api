import json
from pathlib import Path
from sqlite3 import IntegrityError
import uuid
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.api.schemas.chat import ChatCreate, ChatRead, RedisChatMessage
from app.settings import settings
from .routers import api_router
from sqlalchemy.exc import IntegrityError
from app.redis.redis import get_redis
from redis.asyncio.client import Redis # type: ignore

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


APP_ROOT = Path(__file__).parent.parent.parent
app.mount("/photos", StaticFiles(directory=APP_ROOT / "photos"), name="photos")





app.include_router(api_router)

@app.websocket("/ws/{user_id}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, chat_id: str, redis: Redis = Depends(get_redis)):
    await settings.manager.connect(websocket, chat_id)
    try:
        while True:
            chat = await redis.exists(str(chat_id))
            if chat == 0:
                raise HTTPException(status_code=404, detail="Chat not found")
            message = await websocket.receive_text()
            await settings.manager.broadcast(message, chat_id)

            redis_message: RedisChatMessage = RedisChatMessage(
                user_id=user_id,
                message=message
            )

            await redis.rpush(chat_id, redis_message.model_dump_json())
    except WebSocketDisconnect:
        settings.manager.disconnect(websocket, chat_id)
