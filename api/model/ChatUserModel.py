from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatUser(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    chat_id: Optional[str]
    is_admin: Optional[bool] = Field(...)
    created_by: Optional[str] = Field(...)
    created_at: Optional[datetime] = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "some-id",
                "user_id": "some-id",
                "chat_id": "some-id",
                "is_admin": True,
                "created_by": "some-id",
                "created_at": "2022-02-02T12:00:00Z",
            }
        }
    