from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Organisation(Base):
    __tablename__ = 'organisations'
    orgId = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String)

    users = relationship("UserOrganisation", back_populates="organisation")
