from typing import Any, Union
from pydantic import BaseModel


class ParticipantSchema(BaseModel):
    chat_id: str
    user_id: str
    
    class Config:
        schema_extra={
            "example":{
                "chat_id": "some-id",
                "user_id": "some-id"
            }
        }
        

class RequestAddParticipant(BaseModel):
    user_id: Union[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "user_id": "some-id"
            }
        }
        
        
class RequestAddMessage(BaseModel):
    content: Union[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "content": "some-content"
            }
        }
