from pydantic import BaseModel
from typing import List, Optional


class ItemDTO(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None
    owner_id: Optional[int]

    class Config:
        from_attributes = True


class UserDTO(BaseModel):
    id: Optional[int]
    username: str
    email: str
    items: Optional[List[ItemDTO]] = []

    class Config:
        from_attributes = True
