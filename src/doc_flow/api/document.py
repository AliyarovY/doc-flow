from fastapi import (
    APIRouter,
    Depends,
    status,
)

from doc_flow.services.auth import get_current_user

from doc_flow import models
from doc_flow import tables

from doc_flow.services.document import (
    DocService
)


router = APIRouter(
    prefix='/document',
    tags=['document'],
)


@router.post(
    '/create/',
    status_code=status.HTTP_201_CREATED
)
def create_doc(
        doc_data: models.CreateDoc,
        current_user: tables.User = Depends(get_current_user),
        doc_service: DocService = Depends(),
):
    doc_service.create_document(doc_data, current_user)


@router.post(
    '/verify/',
)
def verify_doc(
        doc_data: models.AdminCheckedDoc,
        current_user: tables.User = Depends(get_current_user),
        doc_service: DocService = Depends(),
):
    doc_service.verify_document(doc_data, current_user)
