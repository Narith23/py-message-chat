from typing import Optional, Union
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", primary_key=True, unique=True)
    name: str = Field(...)
    email: Union[str, None] = Field(...)
    phone: Union[str, None] = Field(...)
    password: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@me.com",
                "phone": "1234567890",
                "password": "123456"
            }
        }
    