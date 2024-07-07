from pydantic import BaseModel, Field

class OrganisationBase(BaseModel):
    name: str = Field(..., example="John's Organisation")
    description: str = Field(None, example="An example organisation")

class OrganisationCreate(OrganisationBase):
    pass

class UserOrganisationBase(BaseModel):
    userId: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    orgId: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

class UserOrganisationCreate(UserOrganisationBase):
    pass

class UserOrganisationResponse(UserOrganisationBase):
    id: str

    class Config:
        orm_mode = True
