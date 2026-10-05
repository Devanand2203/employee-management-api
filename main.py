from typing import Literal

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    status,
    Response
)

from sqlalchemy.orm import Session

from database import (
    Base,
    engine,
    get_db
)

from schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeSearchResponse,
    WorkItemCreate,
    WorkItemUpdate,
    WorkItemResponse,
    WorkItemSearchResponse
)

import crud



Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Employee Management API",
    description="Employee CRUD, Search, Filter and Pagination API",
    version="1.0.0"
)

@app.get("/")
def home():

    return {
        "message": "Employee Management API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "message": "Employee Management API is running"
    }

# Employee APIs

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):

    result = crud.create_employee(
        db,
        employee
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return result

@app.get(
    "/employees/search",
    response_model=EmployeeSearchResponse
)
def search_employees(

    name: str | None = None,

    department: str | None = None,

    primary_skill: str | None = None,

    location: str | None = None,

    work_mode: Literal["WFH","WFO"] | None = None,

    is_active: bool | None = None,

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    offset: int = Query(
        default=0,
        ge=0
    ),

    db: Session = Depends(get_db)
):

    employees, total = crud.search_employees(

        db=db,

        name=name,

        department=department,

        primary_skill=primary_skill,

        location=location,

        work_mode=work_mode,

        is_active=is_active,

        limit=limit,

        offset=offset
    )

    return {

        "total": total,

        "limit": limit,

        "offset": offset,

        "employees": employees
    }


@app.get(
    "/employees",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):

    return crud.get_all_employees(db)


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(

    employee_id: int,

    db: Session = Depends(get_db)
):

    if employee_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0"
        )

    employee = crud.get_employee_by_id(
        db,
        employee_id
    )

    if not employee:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(

    employee_id: int,

    employee: EmployeeUpdate,

    db: Session = Depends(get_db)
):

    if employee_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0"
        )

    result = crud.update_employee(
        db,
        employee_id,
        employee
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if result == "duplicate_email":

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return result


@app.delete(
    "/employees/{employee_id}"
)
def delete_employee(

    employee_id: int,

    db: Session = Depends(get_db)
):

    if employee_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0"
        )

    result = crud.delete_employee(
        db,
        employee_id
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    if result == "HAS_WORK_ITEMS":

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete employee because work items are assigned to this employee"
        )

    return {

        "message": "Employee deleted successfully",

        "employee_id": employee_id
    }

#Work Item APIs

@app.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_work_item(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):

    if not work_item.title.strip():

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must not be blank"
        )

    result = crud.create_work_item(
        db,
        work_item
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned employee not found"
        )

    return result

@app.get(
    "/work-items",
    response_model=WorkItemSearchResponse
)
def search_work_items(

    search: str | None = None,

    employee_id: int | None = Query(
        default=None,
        gt=0
    ),

    work_status: str | None = Query(
        default=None,
        alias="status"
    ),

    priority: str | None = None,

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    offset: int = Query(
        default=0,
        ge=0
    ),

    db: Session = Depends(get_db)
):

    if work_status is not None and work_status not in [
        "TODO",
        "IN_PROGRESS",
        "COMPLETED"
    ]:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid status"
        )

    if priority is not None and priority not in [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid priority"
        )

    items, total = crud.search_work_items(

        db=db,

        search=search,

        employee_id=employee_id,

        status=work_status,

        priority=priority,

        limit=limit,

        offset=offset
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items
    }

@app.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item(

    work_item_id: int,

    db: Session = Depends(get_db)
):

    if work_item_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work item ID must be greater than 0"
        )

    work_item = crud.get_work_item_by_id(
        db,
        work_item_id
    )

    if not work_item:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found"
        )

    return work_item

@app.put(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def update_work_item(

    work_item_id: int,

    work_item: WorkItemUpdate,

    db: Session = Depends(get_db)
):

    if work_item_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work item ID must be greater than 0"
        )

    if (
        work_item.title is not None
        and not work_item.title.strip()
    ):

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Title must not be blank"
        )

    result = crud.update_work_item(
        db,
        work_item_id,
        work_item
    )

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found"
        )

    if result == "employee_not_found":

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned employee not found"
        )

    return result

@app.delete(
    "/work-items/{work_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_work_item(

    work_item_id: int,

    db: Session = Depends(get_db)
):

    if work_item_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Work item ID must be greater than 0"
        )

    result = crud.delete_work_item(
        db,
        work_item_id
    )

    if not result:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

