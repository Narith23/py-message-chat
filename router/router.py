import json
from typing import Annotated, Any, List, Union
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    HTTPException,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketState

from api.controller.ChatController import ChatController
from api.controller.UserController import UserController
from api.schema.ParticipantSchema import RequestAddMessage, RequestAddParticipant
from api.schema.UserSchema import UserShema, UserToken
from router.verify_token import get_current_user


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/api/v1/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


router = APIRouter(
    prefix="/api/v1",
)


# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Connection manager for WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# Session Websocket
async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[Union[str, None], Cookie()] = None,
    token: Annotated[Union[str, None], Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


# Chat Router
@router.get("/chats", status_code=status.HTTP_200_OK, tags=["chat".upper()])
async def get_chat(user: UserToken = Depends(get_current_user)):
    return await ChatController.get_chats(user)


@router.post("/chats", status_code=status.HTTP_200_OK, tags=["chat".upper()])
async def add_chat(
    request: RequestAddParticipant, user: UserToken = Depends(get_current_user)
):
    return await ChatController.add_chat(request, user)


@router.get("/chats/{chat_id}", status_code=status.HTTP_200_OK, tags=["chat".upper()])
async def get_chat(chat_id, user: UserToken = Depends(get_current_user)):
    return await ChatController.get_chat(chat_id, user)


@router.put(
    "/chats/{chat_id}/messages", status_code=status.HTTP_200_OK, tags=["chat".upper()]
)
async def add_message(
    chat_id: str,
    request: RequestAddMessage,
    user: UserToken = Depends(get_current_user),
):
    return await ChatController.add_message(chat_id, request, user)


# Home Router
@router.get("", status_code=status.HTTP_200_OK, tags=["home".upper()])
async def home(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})


# Auth Router
@router.get("/login", status_code=status.HTTP_200_OK, tags=["user".upper()])
async def login(request: Request):
    return templates.TemplateResponse(
        "auth/login.html", {"request": request, "title": "Login"}
    )


# User Router
@router.post("/login", status_code=status.HTTP_200_OK, tags=["user".upper()])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await UserController.login(form_data)


@router.post("/user", status_code=status.HTTP_201_CREATED, tags=["user".upper()])
async def create_user(request: UserShema):
    return await UserController.add_user(request)


@router.get("/users", status_code=status.HTTP_200_OK, tags=["user".upper()])
async def get_users(user: UserToken = Depends(get_current_user)):
    return await UserController.get_users(user)


@router.get("/test", status_code=status.HTTP_200_OK, tags=["test".upper()])
async def get():
    return HTMLResponse(html)


# Chat Websocket
@router.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            # check response to send personal message or broadcast
            await manager.send_personal_message(f"You wrote: {data.get('content')}", websocket)
            await manager.broadcast(f"Client says: {data.get('content')}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{chat_id} left the chat")


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
