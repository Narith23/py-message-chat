from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MessageModel(BaseModel):
    id: Optional[str]
    user_id: Optional[str] = Field(...)
    chat_id: Optional[str] = Field(...)
    content: Optional[str] = Field(...)
    created_at: Optional[datetime] = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "some-id",
                "user_id": "some-id",
                "chat_id": "some-id",
                "content": "some-content",
                "created_at": "2022-02-02T12:00:00Z"
            }
        }
    
    