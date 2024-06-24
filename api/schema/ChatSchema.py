from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatSchema(BaseModel):
    is_group: Optional[bool] = False
    name: Optional[str] = None
    created_at: Optional[datetime] = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "is_group": True,
                "name": "My Group",
                "created_at": "2022-02-02T12:00:00Z"
            }
        }
    
    