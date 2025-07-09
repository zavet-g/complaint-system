from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ComplaintCreate(BaseModel):
    text: str

class ComplaintResponse(BaseModel):
    id: int
    status: str
    sentiment: str
    category: Optional[str] = None

    class Config:
        from_attributes = True
        orm_mode = True

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    sentiment: Optional[str] = None
    category: Optional[str] = None 