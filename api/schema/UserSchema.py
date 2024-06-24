from typing import Union
from pydantic import BaseModel


class UserShema(BaseModel):
    name: str
    email: Union[str, None] = None
    phone: Union[str, None] = None
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@me.com",
                "phone": "1234567890",
                "password": "123456"
            }
        }

class UserLogin(BaseModel):
    username: str
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "username": "jdoe@me.com",
                "password": "123456"
            }
        }
        
class UserToken(BaseModel):
    id: str
    name: str
    email: Union[str, None] = None
    phone: Union[str, None] = None
    
    