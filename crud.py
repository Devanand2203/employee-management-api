from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate


def create_employee(
    db: Session,
    employee_data: EmployeeCreate
):

    email = employee_data.email.lower()

    existing_employee = (
        db.query(Employee)
        .filter(
            func.lower(Employee.email) == email
        )
        .first()
    )

    if existing_employee:
        return None

    employee = Employee(
        name=employee_data.name,
        email=email,
        department=employee_data.department,
        primary_skill=employee_data.primary_skill,
        location=employee_data.location,
        work_mode=employee_data.work_mode,
        is_active=employee_data.is_active
    )

    try:

        db.add(employee)

        db.commit()

        db.refresh(employee)

        return employee

    except Exception:

        db.rollback()

        raise


def get_all_employees(db: Session):

    return (
        db.query(Employee)
        .order_by(Employee.id)
        .all()
    )


def get_employee_by_id(
    db: Session,
    employee_id: int
):

    return (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )



def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):

    employee = get_employee_by_id(
        db,
        employee_id
    )

    if not employee:
        return None

    email = employee_data.email.lower()

    duplicate = (
        db.query(Employee)
        .filter(
            func.lower(Employee.email) == email,
            Employee.id != employee_id
        )
        .first()
    )

    if duplicate:
        return "duplicate_email"

    employee.name = employee_data.name
    employee.email = email
    employee.department = employee_data.department
    employee.primary_skill = employee_data.primary_skill
    employee.location = employee_data.location
    employee.work_mode = employee_data.work_mode
    employee.is_active = employee_data.is_active

    try:

        db.commit()

        db.refresh(employee)

        return employee

    except Exception:

        db.rollback()

        raise


def delete_employee(
    db: Session,
    employee_id: int
):

    employee = get_employee_by_id(
        db,
        employee_id
    )

    if not employee:
        return None

    try:

        db.delete(employee)

        db.commit()

        return employee

    except Exception:

        db.rollback()

        raise


def search_employees(
    db: Session,
    name: str | None = None,
    department: str | None = None,
    primary_skill: str | None = None,
    location: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = 10,
    offset: int = 0
):

    query = db.query(Employee)

    if name:

        query = query.filter(
            Employee.name.ilike(
                f"%{name}%"
            )
        )

    if department:

        query = query.filter(
            Employee.department.ilike(
                f"%{department}%"
            )
        )

    if primary_skill:

        query = query.filter(
            Employee.primary_skill.ilike(
                f"%{primary_skill}%"
            )
        )

    if location:

        query = query.filter(
            Employee.location.ilike(
                f"%{location}%"
            )
        )

    if work_mode:

        query = query.filter(
            Employee.work_mode == work_mode
        )

    if is_active is not None:

        query = query.filter(
            Employee.is_active == is_active
        )

    total = query.count()

    employees = (
        query
        .order_by(Employee.id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    return employees, total