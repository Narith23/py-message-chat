from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Participant(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", primary_key=True, unique=True)
    chat_id: Optional[str] = Field(forign_key="Chat.id")
    user_id: Optional[str] = Field(forign_key="User.id")
    created_by: Optional[str] = Field(forign_key="User.id")
    created_at: Optional[datetime] = Field(default=datetime.now())

    class Config:
        schema_extra = {
            "example": {
                "id": "some-id",
                "chat_id": "some-id",
                "user_id": "some-id",
                "created_by": "some-id",
                "created_at": "2022-02-02T12:00:00Z",
            }
        }
