from fastapi import APIRouter

from .prices import router as prc_router
from .storage import router as stor_router
from .matrices import router as mat_router
from .locations import router as loc_router
from .categories import router as cat_router
from .matrix_logs import router as matrix_logs
from .storage_logs import router as storage_logs

api = APIRouter()

api.include_router(prc_router)
api.include_router(mat_router)
api.include_router(loc_router)
api.include_router(cat_router)
api.include_router(stor_router)
api.include_router(matrix_logs)
api.include_router(storage_logs)
