from pydantic import BaseModel, root_validator

from doc_flow import models, tables

from doc_flow.services.utils import get_document


class CreateDoc(BaseModel):
    name: str
    content: str
    admin_id: int


class AdminCheckedDoc(BaseModel):
    id: int
    is_verified: bool
    comment: str = None


class Doc(BaseModel):
    id: int
    name: str
    content: str
    is_verified: bool
    user: models.User
    admin: models.User
