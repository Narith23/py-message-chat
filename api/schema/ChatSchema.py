from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatSchema(BaseModel):
    name: Optional[str] = None
    is_group: Optional[bool] = False
    
    class Config:
        schema_extra = {
            "example": {
                "is_group": True,
                "name": "My Group",
                "created_at": "2022-02-02T12:00:00Z"
            }
        }
