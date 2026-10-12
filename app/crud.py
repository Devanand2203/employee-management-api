from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Employee, WorkItem
from app.schemas import EmployeeCreate, EmployeeUpdate,WorkItemCreate


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

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return None

    work_items=db.query(WorkItem).filter(
        WorkItem.employee_id == employee_id
    ).first()

    if work_items:
        return "HAS_WORK_ITEMS"
    
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

def create_work_item(
    db: Session,
    work_item: WorkItemCreate
):

    employee = db.query(Employee).filter(
        Employee.id == work_item.employee_id
    ).first()

    if not employee:
        return None

    new_work_item = WorkItem(
        title=work_item.title.strip(),
        description=work_item.description,
        employee_id=work_item.employee_id,
        status=work_item.status,
        priority=work_item.priority,
        due_date=work_item.due_date
    )

    try:
       db.add(new_work_item)

       db.commit()

       db.refresh(new_work_item)

       return new_work_item

    except Exception:

       db.rollback()

       raise

def search_work_items(
    db: Session,
    search=None,
    employee_id=None,
    status=None,
    priority=None,
    limit=10,
    offset=0
):

    query = db.query(WorkItem)

    if search:
        query = query.filter(
            WorkItem.title.ilike(f"%{search}%")
        )

    if employee_id is not None:
        query = query.filter(
            WorkItem.employee_id == employee_id
        )

    if status:
        query = query.filter(
            WorkItem.status == status
        )

    if priority:
        query = query.filter(
            WorkItem.priority == priority
        )

    total = query.count()

    items = (
        query
        .order_by(WorkItem.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return items, total

def get_work_item_by_id(
    db: Session,
    work_item_id: int
):

    return db.query(WorkItem).filter(
        WorkItem.id == work_item_id
    ).first()


def delete_work_item(
    db: Session,
    work_item_id: int
):

    existing = db.query(WorkItem).filter(
        WorkItem.id == work_item_id
    ).first()


    if not existing:
        return False

    try:

        db.delete(existing)

        db.commit()

        return True

    except Exception:
        db.rollback()

        raise