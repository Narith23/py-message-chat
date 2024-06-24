from datetime import datetime, timedelta
import logging
from bson import ObjectId
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError, JWTError, jwt
from api.model.UserModel import User
from helper.database import user_collection
from api.schema.UserSchema import UserLogin, UserShema, UserToken
from helper.hash_pass import hash_password, verify_password

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_MINUTES = 60
JWT_SECRET_KEY = "-gZNIH52GyRUXi9hThhTw8Kvbi6UMlgz8UjKHJIL3faJqqAXreq_I0WAdfSqjnxk"
JWT_ALGORITHM = "HS256"


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=float(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=float(JWT_REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
    }


async def login_helper(user) -> dict:
    data = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
    }
    return {
        "access_token": await create_access_token(data),
        "refresh_token": await create_refresh_token(data),
    }


class UserController:
    @staticmethod
    async def login(request: UserLogin):
        try:
            user = await user_collection.find_one({"email": request.username})
            if user is None:
                user = await user_collection.find_one({"phone": request.username})
                if user is None:
                    return JSONResponse(
                        status_code=404, content={"message": "User not found"}
                    )

            if not verify_password(request.password, user["password"]):
                return JSONResponse(
                    status_code=401, content={"message": "Wrong password"}
                )

            return await login_helper(user)
        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"message": "Token expired"})
        except JWTError:
            return JSONResponse(status_code=401, content={"message": "Invalid token"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})

    @staticmethod
    async def add_user(request: UserShema):
        try:
            user = User(
                name=request.name,
                email=request.email,
                phone=request.phone,
                password=hash_password(request.password),
            )
            user.id = str(ObjectId())
            await user_collection.insert_one(user.dict(by_alias=True))
            return JSONResponse(
                status_code=201,
                content={
                    "message": "User created successfully",
                },
            )
        except Exception as e:
            logging.exception(e)
            return JSONResponse(
                status_code=500, content={"message": "Internal server error"}
            )

    @staticmethod
    async def get_users(user: UserToken):
        not_query = {
            "id": {"$not": {"$eq": user.get("id")}},
        }
        users = await user_collection.find(not_query).to_list(100)
        return [user_helper(user) for user in users]
