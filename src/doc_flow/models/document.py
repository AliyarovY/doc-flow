from pydantic import BaseModel


class CreateDoc(BaseModel):
    name: str
    content: str
    admin_id: int


class AdminCheckedDoc(BaseModel):
    id: int
    name: str
    is_verified: bool
