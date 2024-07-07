from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class UserOrganisation(Base):
    __tablename__ = 'user_organisation'
    id = Column(String, primary_key=True, index=True, unique=True)
    userId = Column(String, ForeignKey('users.userId'))
    orgId = Column(String, ForeignKey('organisations.orgId'))

    user = relationship("User", back_populates="organisations")
    organisation = relationship("Organisation", back_populates="users")
