from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from api.controller.ChatController import ChatController
from api.controller.UserController import UserController
from api.schema.UserSchema import UserShema, UserToken
from router.verify_token import get_current_user

router = APIRouter(
    prefix="/api/v1",
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Chat Router
@router.get("/chats", status_code=status.HTTP_200_OK, tags=["chat".upper()])
async def get_chat(user: UserToken = Depends(get_current_user)):
    return await ChatController.get_chats(user)

@router.post("/add/contact", status_code=status.HTTP_200_OK, tags=["chat".upper()])
async def add_contact(contact: str, user: UserToken = Depends(get_current_user)):
    return await ChatController.add_contact(contact, user)

# Home Router
@router.get("", status_code=status.HTTP_200_OK, tags=["home".upper()])
async def home(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})

# Auth Router
@router.get("/login", status_code=status.HTTP_200_OK, tags=["user".upper()])
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request, "title": "Login"})

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
