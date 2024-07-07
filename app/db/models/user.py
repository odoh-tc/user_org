from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = 'users'
    userId = Column(String, primary_key=True, index=True, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    phone = Column(String)

    organisations = relationship("UserOrganisation", back_populates="user")
