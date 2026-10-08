from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


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


class WorkItemBase(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = Field(
        default=None,
        max_length=1000
    )

    employee_id: int = Field(
        ...,
        gt=0
    )

    status: Literal[
        "TODO",
        "IN_PROGRESS",
        "COMPLETED"
    ] = "TODO"

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH"
    ] = "MEDIUM"

    due_date: date | None = None


    @field_validator("title")
    @classmethod
    def validate_title(cls, value):

        if not value.strip():
            raise ValueError(
                "Title cannot be blank"
            )

        return value.strip()

class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    employee_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    status: Optional[
        Literal[
            "TODO",
            "IN_PROGRESS",
            "COMPLETED"
        ]
    ] = None

    priority: Optional[
        Literal[
            "LOW",
            "MEDIUM",
            "HIGH"
        ]
    ] = None

    due_date: Optional[date] = None

    @field_validator(
        "title",
        "employee_id",
        "status",
        "priority",
        mode="before"
    )
    @classmethod
    def reject_null_values(cls, value):

        if value is None:
            raise ValueError(
                "This field cannot be null"
            )

        return value



class AssignedEmployeeResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class WorkItemResponse(BaseModel):

    id: int

    title: str

    description: str | None = None

    employee_id: int

    status: str

    priority: str

    due_date: date | None = None

    created_at: datetime

    employee: AssignedEmployeeResponse

    model_config = {
        "from_attributes": True
    }


class WorkItemSearchResponse(BaseModel):

    total: int

    limit: int

    offset: int

    items: list[WorkItemResponse]