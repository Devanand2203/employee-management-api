from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

class EmployeeBase(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50
    )

    email: EmailStr

    department: str = Field(
        min_length=2,
        max_length=50
    )

    primary_skill: str = Field(
        min_length=2,
        max_length=50
    )

    location: str = Field(
        min_length=2,
        max_length=50
    )

    work_mode: Literal["WFH", "WFO"]

    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):

    id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class EmployeeSearchResponse(BaseModel):

    total: int

    limit: int

    offset: int

    employees: list[EmployeeResponse]