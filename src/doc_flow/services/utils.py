from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from doc_flow import tables
from doc_flow.database import get_session


def get_document(
        id: int,
) -> tables.Document:
    session = next(get_session())

    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Not valid document id',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    doc = (
        session
        .query(tables.Document)
        .filter(
            tables.Document.id == id,
        )
        .first()
    )
    session.close()

    if not doc:
        raise exception from None

    return doc
