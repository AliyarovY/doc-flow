from fastapi import APIRouter

from . import (
    auth,
    document,
)


router = APIRouter()
router.include_router(auth.router)
router.include_router(document.router)

