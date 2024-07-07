from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError
from datetime import timedelta
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.core.utils import generate_uuid
from app.db.models.user import User
from app.db.models.organisation import Organisation
from app.db.models.user_organisation import UserOrganisation
from app.db.schemas.user import UserCreate


def register_user(user: UserCreate, db: Session):
    try:
        user = UserCreate(**user.dict())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail={
            "errors": [
                {
                    "field": error['loc'][1],
                    "message": error['msg']
                } for error in e.errors()
            ]
        })

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            }
        )

    user_model = User(
        userId=generate_uuid(),
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=get_password_hash(user.password),
        phone=user.phone
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    organisation_model = Organisation(
        orgId=generate_uuid(),
        name=f"{user.firstName}'s Organisation",
        description="Default organisation"
    )
    db.add(organisation_model)
    db.commit()
    db.refresh(organisation_model)

    user_organisation = UserOrganisation(
        id=generate_uuid(),
        userId=user_model.userId,
        orgId=organisation_model.orgId
    )
    db.add(user_organisation)
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_model.email}, expires_delta=access_token_expires
    )

    return {
        "status": "success",
        "message": "Registration successful",
        "data": {
            "accessToken": access_token,
            "user": {
                "userId": user_model.userId,
                "firstName": user_model.firstName,
                "lastName": user_model.lastName,
                "email": user_model.email,
                "phone": user_model.phone
            }
        }
    }
