import json
from sqlite3 import IntegrityError
import uuid
from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from app.api.schemas.chat import ChatCreate, ChatRead
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



@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    raise HTTPException(status_code=400, detail=str(exc.orig).split("\nDETAIL:  ")[1])


app.include_router(api_router)

@app.post("/create_chat", response_model=ChatCreate)
async def create_chat(chat: ChatCreate, redis: Redis = Depends(get_redis)):
    # chat_created: ChatRead = ChatRead(
    #     id=uuid.uuid4(),
    #     name=chat.name
    # )
    if await redis.exists(f"chat:{chat.name}"):
        raise HTTPException(status_code=400, detail="Chat already exists")
    # Создание нового чата
    await redis.rpush(f"chat:{chat.name}", json.dumps({"message": "Chat created"}))
    return chat
@app.get("/chats/")
async def get_chats(redis: Redis = Depends(get_redis)):
    chats = await redis.keys("chat:*")
    return {"chats": [chat.decode("utf-8") for chat in chats]}

@app.get("/messages/{chat_id}")
async def get_chats(chat_id: str ,redis: Redis = Depends(get_redis)):
    chat = await redis.exists(f"chat:{chat_id}")
    if chat == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    messages = await redis.lrange(f"chat:{chat_id}", 0, -1)
    return {"chat_id": chat_id, "messages": [json.loads(message.decode("utf-8")) for message in messages]}
# @app.get("/messages/{chat_id}")
# async def get_messages(chat_id: str):
#     messages = await redis.lrange(f"chat:{chat_id}", 0, -1)
#     return {"chat_id": chat_id, "messages": [message.decode("utf-8") for message in messages]}
@app.websocket("/ws/{user_id}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, chat_id: str, redis: Redis = Depends(get_redis)):
    await settings.manager.connect(websocket, chat_id)
    try:
        while True:
            chat = await redis.exists(f"chat:{chat_id}")
            if chat == 0:
                raise HTTPException(status_code=404, detail="Chat not found")
            message = await websocket.receive_text()
            await settings.manager.broadcast(message, chat_id)

            data = json.dumps({
                    "user_id": user_id,
                    "message": message})

            await redis.rpush(f"chat:{chat_id}", data)
    except WebSocketDisconnect:
        settings.manager.disconnect(websocket, chat_id)
