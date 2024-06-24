from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MessageModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", primary_key=True, unique=True)
    chat_id: Optional[str] = Field(..., forign_key="Chat.id")
    user_id: Optional[str] = Field(..., forign_key="User.id")
    content: Optional[str] = Field(...)
    created_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "some-id",
                "chat_id": "some-id",
                "user_id": "some-id",
                "content": "some-content",
                "created_at": "2022-02-02T12:00:00Z",
                "updated_at": "2022-02-02T12:00:00Z"
            }
        }
    
    