from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.schemas.organisation import OrganisationCreate
from app.core.security import get_current_user
from app.db.session import get_db
from app.services.organisation import (
    get_organisations,
    get_organisation,
    create_organisation,
    add_user_to_organisation,
)

router = APIRouter(prefix="/api/organisations", tags=["organisations"])

@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
def get_organisations_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_organisations(db, current_user)

@router.get("/{orgId}", response_model=dict, status_code=status.HTTP_200_OK)
def get_organisation_route(orgId: str = Path(..., title="Organisation ID"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_organisation(orgId, db, current_user)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_organisation_route(org: OrganisationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_organisation(org, db, current_user)

@router.post("/{orgId}/users")
def add_user_to_organisation_route(orgId: str, userId: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return add_user_to_organisation(orgId, userId, db)

