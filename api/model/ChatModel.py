from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: Optional[str]
    is_group: Optional[bool] = Field(...)
    name: Optional[str] = Field(...)
    created_at: Optional[datetime] = Field(...)
    user_id: Optional[str] = Field(...)
    created_by: Optional[str] = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "id": "some-id",
                "is_group": True,
                "name": "My Group",
                "created_at": "2022-02-02T12:00:00Z",
                "user_id": "some-id",
                "created_by": "some-id"
            }
        }
    
    