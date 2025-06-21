from pydantic import BaseModel, EmailStr
from typing import Optional, List

class IdentifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None

class IdentifyResponse(BaseModel):
    contact: dict