from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Employee, WorkItem
from app.schemas import WorkItemUpdate


ALLOWED_TRANSITIONS = {
    "TODO": "IN_PROGRESS",
    "IN_PROGRESS": "COMPLETED",
}


def change_work_item_status(
    db: Session,
    work_item_id: int,
    requested_status: str
):
    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        return None

    current_status = work_item.status

    # Requesting the current status is allowed.
    if requested_status == current_status:
        return work_item

    # Only allow the next status in the workflow.
    if ALLOWED_TRANSITIONS.get(current_status) != requested_status:
        return "invalid_status_transition"

    try:
        work_item.status = requested_status

        db.commit()
        db.refresh(work_item)

        return work_item

    except Exception:
        db.rollback()
        raise


def update_work_item(
    db: Session,
    work_item_id: int,
    work_item_data: WorkItemUpdate
):
    existing = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if existing is None:
        return None

    update_data = work_item_data.model_dump(
        exclude_unset=True
    )

    # Validate the status transition before changing
    # any other field. A rejected transition must not
    # partially update the work item.
    if "status" in update_data:
        requested_status = update_data["status"]

        if requested_status != existing.status:
            if (
                ALLOWED_TRANSITIONS.get(existing.status)
                != requested_status
            ):
                return "invalid_status_transition"

    # Validate the new employee before changing fields.
    if "employee_id" in update_data:
        employee = (
            db.query(Employee)
            .filter(
                Employee.id == update_data["employee_id"]
            )
            .first()
        )

        if employee is None:
            return "employee_not_found"

    try:
        if "title" in update_data:
            existing.title = update_data["title"].strip()

        if "description" in update_data:
            existing.description = update_data["description"]

        if "employee_id" in update_data:
            existing.employee_id = update_data["employee_id"]

        if "status" in update_data:
            existing.status = update_data["status"]

        if "priority" in update_data:
            existing.priority = update_data["priority"]

        if "due_date" in update_data:
            existing.due_date = update_data["due_date"]

        db.commit()
        db.refresh(existing)

        return existing

    except Exception:
        db.rollback()
        raise


def get_employee_work_summary(
    db: Session,
    employee_id: int
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        return None

    # Count the work items currently assigned to this employee.
    status_counts = (
        db.query(
            WorkItem.status,
            func.count(WorkItem.id)
        )
        .filter(
            WorkItem.employee_id == employee_id
        )
        .group_by(WorkItem.status)
        .all()
    )

    counts = {
        "TODO": 0,
        "IN_PROGRESS": 0,
        "COMPLETED": 0,
    }

    for item_status, count in status_counts:
        if item_status in counts:
            counts[item_status] = count

    total = sum(counts.values())

    return {
        "employee_id": employee_id,
        "total_work_items": total,
        "todo": counts["TODO"],
        "in_progress": counts["IN_PROGRESS"],
        "completed": counts["COMPLETED"],
    }