from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    status
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
    EmployeeSearchResponse
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

    work_mode: str | None = None,

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

    employee = crud.delete_employee(
        db,
        employee_id
    )

    if not employee:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return {

        "message": "Employee deleted successfully",

        "employee_id": employee_id
    }