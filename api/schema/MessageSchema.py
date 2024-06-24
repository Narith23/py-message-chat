from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageShema(BaseModel):
    user_id: Optional[str]
    chat_id: Optional[str]
    content: Optional[str]
    created_at: Optional[datetime] = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "some-id",
                "chat_id": "some-id",
                "content": "some-content",
                "created_at": "2022-02-02T12:00:00Z"
            }
        }
    