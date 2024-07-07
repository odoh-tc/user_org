from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models.user import User
from app.db.models.user_organisation import UserOrganisation



def get_user(id: str, db: Session, current_user: User):
    user = db.query(User).filter(User.userId == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_data = {
        "userId": user.userId,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "email": user.email,
        "phone": user.phone
    }

    # Check if the current user is the same as the requested user
    if current_user.userId == user.userId:
        return {
            "status": "success",
            "message": "User data fetched successfully",
            "data": user_data
        }

    # Check if the current user belongs to the same organisation as the requested user
    current_user_orgs = db.query(UserOrganisation).filter(UserOrganisation.userId == current_user.userId).all()
    user_orgs = db.query(UserOrganisation).filter(UserOrganisation.userId == user.userId).all()
    if any(org.orgId in [user_org.orgId for user_org in user_orgs] for org in current_user_orgs):
        return {
            "status": "success",
            "message": "User data fetched successfully",
            "data": user_data
        }

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user")
