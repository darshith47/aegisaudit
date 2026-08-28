from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.models.user import User
from app.core.security import get_current_user
from app.adapters.registry import engine_registry

router = APIRouter(prefix="/engines", tags=["Security Engine Matrix"])


@router.get("/", response_model=List[Dict[str, Any]])
def get_engine_matrix(current_user: User = Depends(get_current_user)):
    """Retrieve Security Engine capability matrix (Implemented vs Planned engines)."""
    return engine_registry.get_engine_matrix()
