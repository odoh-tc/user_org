from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    firstName: str = Field(..., example="John")
    lastName: str = Field(..., example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    phone: str = Field(None, example="1234567890")

class UserCreate(UserBase):
    password: str = Field(..., example="password123")

class UserResponse(UserBase):
    userId: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="password123")
