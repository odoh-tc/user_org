from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.core.security import get_current_user
from app.db.session import get_db
from app.services.user import get_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
def get_user_route(
    id: str = Path(..., title="User ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user(id, db, current_user)




