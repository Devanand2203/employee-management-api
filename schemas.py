from datetime import date, datetime
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

class WorkItemBase(BaseModel):

    title: str = Field(
        min_length=1,
        max_length=255
    )

    description: str | None = None

    employee_id: int = Field(
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


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    description: str | None = None

    employee_id: int | None = Field(
        default=None,
        gt=0
    )

    status: Literal[
        "TODO",
        "IN_PROGRESS",
        "COMPLETED"
    ] | None = None

    priority: Literal[
        "LOW",
        "MEDIUM",
        "HIGH"
    ] | None = None

    due_date: date | None = None


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