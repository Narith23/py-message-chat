from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Chat(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", primary_key=True, unique=True)
    name: Optional[str] = Field(default=None)
    is_group: Optional[bool] = Field(default=False)
    created_by: Optional[str] = Field(...)
    created_at: Optional[datetime] = Field(default=datetime.now())
    
    class Config:
        schema_extra = {
            "example": {
                "id": "some-id",
                "name": "My Group",
                "is_group": True,
                "created_by": "some-id",
                "created_at": "2022-02-02T12:00:00Z"
            }
        }
    
    