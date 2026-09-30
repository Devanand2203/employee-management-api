#Temporary storage for employee


from datetime import datetime, timezone

employees = []
next_id = 1


def create_employee(employee_data):
    global next_id

    employee = {
        "id": next_id,
        "name": employee_data.name,
        "email": employee_data.email,
        "department": employee_data.department,
        "primary_skill": employee_data.primary_skill,
        "location": employee_data.location,
        "work_mode": employee_data.work_mode,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    }

    employees.append(employee)
    next_id += 1

    return employee


def get_all_employees():
    return employees


def get_employee(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


def update_employee(employee_id, employee_data):
    employee = get_employee(employee_id)

    if employee is None:
        return None

    employee["name"] = employee_data.name
    employee["email"] = employee_data.email
    employee["department"] = employee_data.department
    employee["primary_skill"] = employee_data.primary_skill
    employee["location"] = employee_data.location
    employee["work_mode"] = employee_data.work_mode
    employee["is_active"] = employee_data.is_active

    return employee


def delete_employee(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return False

    employees.remove(employee)
    return True