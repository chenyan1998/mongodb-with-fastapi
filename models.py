from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
from schemas import PyObjectId

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    department: str = Field(...)
    number_employee: float = Field(..., le=100.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "department": "IT",
                "number_employee": "11.0",
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    department: Optional[str]
    number_employee: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "department": "IT",
                "number_employee": "11.0",
            }
        }


class EmployeeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    department: str = Field(...)
    employee_details: str = Field(...)
    employee_risk_level: float = Field(..., le=10.0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "department": "IT",
                "employee_details": "details",
                "employee_risk_level":"3.0",
            }
        }


class UpdateEmployeeModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    department: Optional[str]
    employee_details: Optional[str]
    employee_risk_level: Optional[float]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "department" : "IT",
                "employee_details": "details",
                "employee_risk_level":"3.0",
            }
        }