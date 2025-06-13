import json
from pathlib import Path

from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.api.schemas.chat_message import ChatMessageCreate
from app.api.services.chat_message import ChatMessageService
from app.db.db import get_session
from app.settings import settings

from .routers import api_router

app = FastAPI(
    title=settings.PROJECT_TITLE, version="1.0.0", root_path=settings.FAST_API_PREFIX
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


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: str):
        self.active_connections[chat_id].remove(websocket)
        if not self.active_connections[chat_id]:
            del self.active_connections[chat_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, data, chat_id: str):
        for connection in self.active_connections.get(chat_id, []):
            await connection.send_json(data)


class Settings:
    WS_PREFIX = settings.WS_PREFIX
    manager = ConnectionManager()


ws_settings = Settings()


@app.websocket(f"{ws_settings.WS_PREFIX}/{{user_id}}/{{chat_id}}")
async def websocket_endpoint(
    websocket: WebSocket, user_id: str, chat_id: str, session=Depends(get_session)
):
    await ws_settings.manager.connect(websocket, chat_id)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            chat_message = ChatMessageCreate(
                chat_id=chat_id,
                user_id=user_id,
                message=data["message"],
                file=data.get("file"),
            )
            result = await ChatMessageService(session).create(chat_message)
            result = result.model_dump()
            result["id"] = str(result["id"])
            result["user"]["id"] = str(result["user"]["id"])
            await ws_settings.manager.broadcast(result, chat_id)
    except WebSocketDisconnect:
        ws_settings.manager.disconnect(websocket, chat_id)
