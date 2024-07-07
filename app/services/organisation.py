from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.organisation import Organisation
from app.db.models.user import User
from app.db.models.user_organisation import UserOrganisation
from app.db.schemas.organisation import OrganisationCreate
from app.core.utils import generate_uuid




def get_organisations(db: Session, current_user: User):
    organisations = db.query(Organisation).join(UserOrganisation).filter(UserOrganisation.userId == current_user.userId).all()
    return {
        "status": "success",
        "message": "Organisations fetched successfully",
        "data": {
            "organisations": [
                {
                    "orgId": org.orgId,
                    "name": org.name,
                    "description": org.description,
                }
                for org in organisations
            ]
        }
    }




def get_organisation(orgId: str, db: Session, current_user: User):
    organisation = db.query(Organisation).filter(Organisation.orgId == orgId).first()
    if not organisation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organisation not found")
    if not any(org.orgId == orgId for org in current_user.organisations):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this organisation")

    return {
        "status": "success",
        "message": "Organisation details fetched successfully",
        "data": {
            "orgId": organisation.orgId,
            "name": organisation.name,
            "description": organisation.description,
        }
    }





def create_organisation(org: OrganisationCreate, db: Session, current_user: User):
    try:
        organisation_model = Organisation(
            orgId=generate_uuid(),
            name=org.name,
            description=org.description
        )
        db.add(organisation_model)
        db.commit()
        db.refresh(organisation_model)

        # Link user to organisation
        user_organisation = UserOrganisation(
            id=generate_uuid(),
            userId=current_user.userId,
            orgId=organisation_model.orgId
        )
        db.add(user_organisation)
        db.commit()

        return {
            "status": "success",
            "message": "Organisation created successfully",
            "data": {
                "orgId": organisation_model.orgId,
                "name": organisation_model.name,
                "description": organisation_model.description
            }
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client error")






def add_user_to_organisation(orgId: str, userId: str, db: Session):
    organisation = db.query(Organisation).filter(Organisation.orgId == orgId).first()
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found")
    
    if not userId:
        raise HTTPException(status_code=400, detail="userId field is required in the request body")
    
    user = db.query(User).filter(User.userId == userId).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with userId {userId} not found")
    
    # Check if the user is already linked to the organisation
    existing_link = db.query(UserOrganisation).filter_by(userId=userId, orgId=orgId).first()
    if existing_link:
        raise HTTPException(status_code=400, detail=f"User with userId {userId} is already linked to this organisation")
    
    user_organisation = UserOrganisation(
        id=generate_uuid(),
        userId=userId,
        orgId=orgId
    )
    db.add(user_organisation)
    db.commit()

    return {
        "status": "success",
        "message": "User added to organisation successfully"
    }
