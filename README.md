# Employee Management API

A backend REST API built using **FastAPI, Python, MySQL, and SQLAlchemy** to manage employee records and work items.

The project demonstrates CRUD operations, request validation, database integration, search and filtering, pagination, error handling, foreign-key relationships, SQLAlchemy ORM relationships, and Swagger API documentation.

---

# Features

## Employee Management

* Employee CRUD operations
* MySQL database integration
* SQLAlchemy ORM
* Pydantic request and response validation
* Email validation
* Case-insensitive email uniqueness
* Search employees by name
* Filter employees by department
* Filter employees by work mode
* Pagination using `limit` and `offset`
* Total employee count
* Employee health check endpoint
* Error handling with appropriate HTTP status codes

## Work Item Management

* Create and assign work items to existing employees
* Retrieve all work items
* Retrieve a work item by ID
* Update work item details
* Reassign a work item to another employee
* Delete work items
* Partial and case-insensitive title search
* Filter by employee
* Filter by status
* Filter by priority
* Combined filtering
* Pagination using `limit` and `offset`
* Total matching work item count before pagination
* Ascending ordering by work item ID
* Work item status validation
* Work item priority validation
* Blank/whitespace-only title validation
* Maximum 255-character title validation
* Positive `employee_id` validation
* Employee existence validation
* Assigned employee details included in work item responses
* SQLAlchemy foreign key and relationship between employees and work items

---

# Technologies Used

* **Python**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy**
* **MySQL**
* **PyMySQL**
* **Uvicorn**
* **python-dotenv**
* **email-validator**
* **Swagger UI**

---

# Project Structure

```text
FRAMEWORK/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
│
├── screenshots/
│   ├── gethealth.jpg
│   ├── getempresbod.jpg
│   ├── updempbod.jpg
│   ├── delempresbod.jpg
│   ├── namesearch.jpg
│   ├── searchbydept.jpg
│   ├── workmodevalidator.jpg
│   ├── post_work_items.jpg
│   ├── work_item_by_id.jpg
│   ├── search_by_work_item_title.jpg
│   ├── invalid_status&priority.jpg
│   ├── nonexisting_emp_id.jpg
│   ├── pagination_by_limit&offset.jpg
│   ├── filterbyemp_status_priority.jpg
│   ├── delete_work_item.jpg
│   ├── blanktitle.jpg
│   └── assign_to_another_employee.jpg
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## 1. Clone the Repository

Clone the project repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd FRAMEWORK
```

---

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

After activation, the terminal should show:

```text
(venv)
```

---

## 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

# Database Configuration

This project uses **MySQL** as the database.

Make sure MySQL Server is installed and running on the system.

Create the database:

```sql
CREATE DATABASE employee_db;
```

The application uses SQLAlchemy to connect FastAPI to MySQL.

---

# Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_db
```

## `.env.example`

The repository also contains a `.env.example` file with dummy values:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=employee_db
```

Do not commit the actual `.env` file containing your database password.

---

# Running the Application

Start the FastAPI application using Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

The application will start at:

```text
http://127.0.0.1:8000
```

The `app.main:app` command refers to:

* `app` → Python package
* `main` → `main.py`
* `app` → FastAPI application instance

---

# API Documentation

FastAPI automatically provides interactive API documentation.

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

* View available endpoints
* Check request and response schemas
* Enter request data
* Execute API requests
* View HTTP status codes
* Test validation and error responses

## ReDoc

Alternative API documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

---

# Employee API

The Employee API provides operations for creating, viewing, updating, deleting, searching, and filtering employee records.

## Employee Fields

| Field           | Description                |
| --------------- | -------------------------- |
| `id`            | Auto-generated employee ID |
| `name`          | Employee name              |
| `email`         | Employee email address     |
| `department`    | Employee department        |
| `primary_skill` | Primary technical skill    |
| `location`      | Employee location          |
| `work_mode`     | WFH or WFO                 |
| `is_active`     | Employee active status     |
| `created_at`    | Record creation date       |

---

# Employee Endpoints

## Create Employee

```http
POST /employees
```

Example request:

```json
{
  "name": "Stephen",
  "email": "stephen@example.com",
  "department": "Testing",
  "primary_skill": "Python",
  "location": "Chennai",
  "work_mode": "WFH",
  "is_active": true
}
```

Successful creation returns:

```text
201 Created
```

---

## Get All Employees

```http
GET /employees
```

Returns a list of employee records.

---

## Get Employee by ID

```http
GET /employees/{employee_id}
```

Example:

```text
GET /employees/1
```

---

## Update Employee

```http
PUT /employees/{employee_id}
```

Example:

```text
PUT /employees/1
```

---

## Delete Employee

```http
DELETE /employees/{employee_id}
```

Example:

```text
DELETE /employees/1
```

Successful deletion returns:

```text
204 No Content
```

Employees with existing work items cannot be deleted.

---

# Employee Search and Filtering

The API supports searching and filtering using query parameters.

```http
GET /employees/search
```

## Search by Name

```text
/employees/search?name=Stephen
```

## Filter by Department

```text
/employees/search?department=Testing
```

## Filter by Work Mode

```text
/employees/search?work_mode=WFH
```

## Combine Filters

```text
/employees/search?name=Stephen&department=Testing&work_mode=WFH
```

---

# Work Mode Validation

The `work_mode` field accepts only:

```text
WFH
WFO
```

## Valid Example

```json
{
  "work_mode": "WFH"
}
```

or:

```json
{
  "work_mode": "WFO"
}
```

## Invalid Example

```json
{
  "work_mode": "HYBRID"
}
```

An unsupported work mode returns:

```text
422 Unprocessable Entity
```

---

# Employee Pagination

The employee search endpoint supports pagination using:

* `limit`
* `offset`

Example:

```text
/employees/search?limit=5&offset=0
```

This returns the first 5 records.

To retrieve the next set:

```text
/employees/search?limit=5&offset=5
```

| Parameter | Description                        |
| --------- | ---------------------------------- |
| `limit`   | Maximum number of records returned |
| `offset`  | Number of records skipped          |

Example:

```text
limit=5
offset=10
```

This means:

> Skip the first 10 records and return the next 5 records.

---

# Work Item Management

Task 4 extends the Employee Management API by introducing a new `work_items` table.

Each work item is assigned to an existing employee.

The relationship is:

```text
Employee
   │
   │ 1
   │
   │
   │ many
   ▼
Work Item
```

One employee can have multiple work items.

Each work item belongs to one employee.

---

# Work Items Table

The `work_items` table contains the following fields:

| Field         | Description                                      |
| ------------- | ------------------------------------------------ |
| `id`          | Auto-generated primary key                       |
| `title`       | Required work item title, maximum 255 characters |
| `description` | Optional description                             |
| `employee_id` | ID of the assigned employee                      |
| `status`      | TODO, IN_PROGRESS or COMPLETED                   |
| `priority`    | LOW, MEDIUM or HIGH                              |
| `due_date`    | Optional due date                                |
| `created_at`  | Automatically generated date/time                |

Default values:

```text
status   = TODO
priority = MEDIUM
```

---

# Employee–Work Item Relationship

The `work_items.employee_id` column is a foreign key referencing:

```text
employees.id
```

Conceptually:

```text
employees
    │
    │ 1
    │
    │
    │ *
    ▼
work_items
```

The SQLAlchemy relationship allows the application to access the assigned employee from a work item.

The relationship is a one-to-many relationship:

```text
One Employee ──────── Many Work Items
```

---

# Work Item Status

Only the following status values are accepted:

```text
TODO
IN_PROGRESS
COMPLETED
```

The default status is:

```text
TODO
```

Example:

```json
{
  "status": "IN_PROGRESS"
}
```

An invalid status returns:

```text
422 Unprocessable Entity
```

---

# Work Item Priority

Only the following priority values are accepted:

```text
LOW
MEDIUM
HIGH
```

The default priority is:

```text
MEDIUM
```

An invalid priority returns:

```text
422 Unprocessable Entity
```

---

# Work Item Endpoints

## Create Work Item

```http
POST /work-items
```

Creates a work item and assigns it to an existing employee.

Example request:

```json
{
  "title": "Prepare weekly status report",
  "description": "Prepare and submit the weekly project status report",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-10"
}
```

Successful creation returns:

```text
201 Created
```

Example response:

```json
{
  "id": 1,
  "title": "Prepare weekly status report",
  "description": "Prepare and submit the weekly project status report",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-10",
  "created_at": "2026-10-04T01:20:00",
  "employee": {
    "id": 2,
    "name": "Employee Name",
    "email": "employee@example.com"
  }
}
```

If the assigned employee does not exist:

```text
404 Not Found
```

---

# Get Work Items

```http
GET /work-items
```

Returns work items with optional search, filtering, and pagination.

## Query Parameters

| Parameter     | Description                               | Default |
| ------------- | ----------------------------------------- | ------- |
| `search`      | Partial, case-insensitive search on title | None    |
| `employee_id` | Filter by assigned employee               | None    |
| `status`      | Filter by status                          | None    |
| `priority`    | Filter by priority                        | None    |
| `limit`       | Number of records returned                | 10      |
| `offset`      | Number of records skipped                 | 0       |

---

# Search Work Items by Title

Example:

```text
GET /work-items?search=report
```

The search is:

* Partial
* Case-insensitive
* Performed on the work item title

For example, searching for:

```text
report
```

can match titles such as:

```text
Prepare Weekly Report
Monthly Report
Project Report
```

---

# Filter by Employee

```text
GET /work-items?employee_id=2
```

Returns work items assigned to employee `2`.

---

# Filter by Status

```text
GET /work-items?status=IN_PROGRESS
```

Returns only work items with `IN_PROGRESS` status.

---

# Filter by Priority

```text
GET /work-items?priority=HIGH
```

Returns only work items with `HIGH` priority.

---

# Combined Filters

All supplied filters can be used together.

Example:

```text
GET /work-items?employee_id=2&status=TODO&priority=HIGH
```

The response contains only records matching all supplied filters.

---

# Work Item Pagination

Work item pagination uses:

* `limit`
* `offset`

Example:

```text
GET /work-items?limit=10&offset=0
```

Another page:

```text
GET /work-items?limit=10&offset=10
```

The allowed values are:

| Parameter | Rule                               |
| --------- | ---------------------------------- |
| `limit`   | Default 10, minimum 1, maximum 100 |
| `offset`  | Default 0, minimum 0               |

Work items are returned in ascending order by ID.

Filtering, counting, ordering, and pagination are performed using SQLAlchemy queries.

---

# Work Item List Response

The list response follows this format:

```json
{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": []
}
```

The `total` value represents the number of records matching the supplied filters **before `limit` and `offset` are applied**.

---

# Get Work Item by ID

```http
GET /work-items/{work_item_id}
```

Example:

```text
GET /work-items/1
```

Returns the work item and basic details of the assigned employee.

If the work item does not exist:

```text
404 Not Found
```

---

# Update Work Item

```http
PUT /work-items/{work_item_id}
```

Updates work item details or assigns the work item to another employee.

Example:

```text
PUT /work-items/1
```

Example request:

```json
{
  "title": "Prepare updated weekly report",
  "description": "Update the weekly project report",
  "employee_id": 3,
  "status": "IN_PROGRESS",
  "priority": "HIGH",
  "due_date": "2026-10-12"
}
```

The work item can be reassigned by changing `employee_id`.

The new employee must already exist.

If the employee does not exist:

```text
404 Not Found
```

If the work item does not exist:

```text
404 Not Found
```

---

# Delete Work Item

```http
DELETE /work-items/{work_item_id}
```

Example:

```text
DELETE /work-items/1
```

Successful deletion returns:

```text
204 No Content
```

If the work item does not exist:

```text
404 Not Found
```

---

# Work Item Response

Every work item response includes basic details of the assigned employee.

Example:

```json
{
  "id": 1,
  "title": "Prepare weekly status report",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "employee": {
    "id": 2,
    "name": "Employee Name",
    "email": "employee@example.com"
  }
}
```

The `employee` field is provided through the SQLAlchemy relationship between `Employee` and `WorkItem`.

---

# Work Item Validation and Business Rules

## Title

The title is required and must not be empty.

The title must contain at least one non-whitespace character.

The maximum title length is:

```text
255 characters
```

Invalid examples:

```json
{
  "title": ""
}
```

and:

```json
{
  "title": "   "
}
```

Blank or whitespace-only titles are rejected with:

```text
422 Unprocessable Entity
```

A title exceeding 255 characters is also rejected with:

```text
422 Unprocessable Entity
```

---

## Employee ID

`employee_id` must be a positive integer.

Valid:

```json
{
  "employee_id": 1
}
```

Invalid:

```json
{
  "employee_id": 0
}
```

Invalid:

```json
{
  "employee_id": -1
}
```

Values of `0` or below return:

```text
422 Unprocessable Entity
```

The employee must also exist in the database.

A nonexistent employee returns:

```text
404 Not Found
```

For work item creation, `employee_id` is required.

For work item updates, `employee_id` may be omitted, but when provided it must be greater than `0`.

---

## Status Validation

Valid values:

```text
TODO
IN_PROGRESS
COMPLETED
```

Invalid status values return:

```text
422 Unprocessable Entity
```

---

## Priority Validation

Valid values:

```text
LOW
MEDIUM
HIGH
```

Invalid priority values return:

```text
422 Unprocessable Entity
```

---

# SQLAlchemy Foreign Key and Relationship

The `WorkItem` model uses a foreign key to connect each work item to an employee.

Conceptually:

```python
employee_id = Column(
    Integer,
    ForeignKey("employees.id"),
    nullable=False
)
```

The `Employee` model has a relationship to work items:

```python
work_items = relationship(
    "WorkItem",
    back_populates="employee"
)
```

The `WorkItem` model has the corresponding relationship:

```python
employee = relationship(
    "Employee",
    back_populates="work_items"
)
```

This creates the following relationship:

```text
Employee
   │
   ├── Work Item 1
   ├── Work Item 2
   └── Work Item 3
```

---

# Database

The application uses:

```text
MySQL
```

Database name:

```text
employee_db
```

The database contains employee and work item data.

SQLAlchemy is used as the ORM layer.

SQLAlchemy is responsible for:

* Defining database models
* Creating database queries
* Inserting records
* Updating records
* Deleting records
* Retrieving records
* Managing database sessions
* Handling employee/work-item relationships

---

# Data Persistence

Work item records are stored in MySQL.

Therefore, restarting the FastAPI application does not remove existing records.

After stopping and restarting the application:

```bash
python -m uvicorn app.main:app --reload
```

existing records can still be retrieved through:

```text
GET /work-items
```

This confirms that records are persisted in the database rather than being stored only in application memory.

---

# Validation

The API uses Pydantic for request validation.

Validation includes:

* Required fields
* Email format
* String validation
* Numeric validation
* Work mode validation
* Work item status validation
* Work item priority validation
* Positive employee ID validation
* Pagination validation
* Blank title validation
* Maximum 255-character title validation
* Request body validation

Invalid requests return appropriate FastAPI validation errors.

Example:

```text
422 Unprocessable Entity
```

---

# Error Handling

The API handles common errors such as:

* Employee not found
* Work item not found
* Invalid employee ID
* Duplicate employee email
* Invalid request body
* Invalid work mode
* Invalid work item status
* Invalid work item priority
* Blank work item title
* Title exceeding 255 characters
* Database-related errors

Example:

```json
{
  "detail": "Employee not found"
}
```

---

# Testing

The API can be tested using:

* Swagger UI
* Postman
* Browser for GET requests

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Task 4 Testing Checklist

The following Work Item API scenarios should be tested.

## 1. Create a Work Item for an Existing Employee

```text
POST /work-items
```

Expected:

```text
201 Created
```

---

## 2. Assign a Work Item to a Nonexistent Employee

Use an employee ID that does not exist.

Expected:

```text
404 Not Found
```

---

## 3. Retrieve a Work Item by ID

```text
GET /work-items/{work_item_id}
```

Expected:

```text
200 OK
```

---

## 4. Search Using Part of a Work Item Title

```text
GET /work-items?search=report
```

Expected:

* Partial title matching
* Case-insensitive search

---

## 5. Filter by Employee

```text
GET /work-items?employee_id=2
```

---

## 6. Filter by Status

```text
GET /work-items?status=IN_PROGRESS
```

---

## 7. Filter by Priority

```text
GET /work-items?priority=HIGH
```

---

## 8. Test Combined Filters

Example:

```text
GET /work-items?employee_id=2&status=TODO&priority=HIGH
```

Expected:

Only records matching all supplied filters are returned.

---

## 9. Test Pagination

First page:

```text
GET /work-items?limit=2&offset=0
```

Second page:

```text
GET /work-items?limit=2&offset=2
```

Expected:

* `limit` controls returned records
* `offset` controls skipped records
* `total` remains the total matching record count before pagination

---

## 10. Test Invalid Status

Example:

```text
GET /work-items?status=INVALID
```

Expected:

```text
422 Unprocessable Entity
```

---

## 11. Test Invalid Priority

Example:

```text
GET /work-items?priority=INVALID
```

Expected:

```text
422 Unprocessable Entity
```

---

## 12. Test Blank Title Validation

Example:

```json
{
  "title": "   ",
  "employee_id": 1
}
```

Expected:

```text
422 Unprocessable Entity
```

---

## 13. Test Title Length Validation

A title containing more than 255 characters should be rejected.

Expected:

```text
422 Unprocessable Entity
```

---

## 14. Test Invalid Employee ID

Example:

```json
{
  "title": "Prepare report",
  "employee_id": 0
}
```

Expected:

```text
422 Unprocessable Entity
```

The same applies to negative values such as:

```json
{
  "title": "Prepare report",
  "employee_id": -1
}
```

---

## 15. Test Missing Work Item

Example:

```text
GET /work-items/99999
```

Expected:

```text
404 Not Found
```

---

## 16. Update and Assign to Another Employee

```text
PUT /work-items/1
```

Change the `employee_id` to another existing employee.

Expected:

* Work item is updated
* Assignment is changed
* New employee details are returned

---

## 17. Delete a Work Item

```text
DELETE /work-items/1
```

Expected:

```text
204 No Content
```

---

## 18. Restart the Application

Stop the application and restart it:

```bash
python -m uvicorn app.main:app --reload
```

Then:

```text
GET /work-items
```

Expected:

* Previously created records remain available
* Records are persisted in MySQL

---

## 19. Confirm Existing Employee APIs

Verify that the Employee APIs continue working after Task 4.

```text
POST /employees

GET /employees

GET /employees/{employee_id}

PUT /employees/{employee_id}

DELETE /employees/{employee_id}

GET /employees/search

GET /health
```

No regression should occur in the existing Employee functionality.

---

# API Summary

| Method | Endpoint                     | Purpose                       | Success |
| ------ | ---------------------------- | ----------------------------- | ------- |
| POST   | `/employees`                 | Create employee               | 201     |
| GET    | `/employees`                 | Get employees                 | 200     |
| GET    | `/employees/{employee_id}`   | Get employee by ID            | 200     |
| PUT    | `/employees/{employee_id}`   | Update employee               | 200     |
| DELETE | `/employees/{employee_id}`   | Delete employee               | 204     |
| GET    | `/employees/search`          | Search/filter employees       | 200     |
| GET    | `/health`                    | Health check                  | 200     |
| POST   | `/work-items`                | Create work item              | 201     |
| GET    | `/work-items`                | List/search/filter work items | 200     |
| GET    | `/work-items/{work_item_id}` | Get work item by ID           | 200     |
| PUT    | `/work-items/{work_item_id}` | Update/reassign work item     | 200     |
| DELETE | `/work-items/{work_item_id}` | Delete work item              | 204     |

---

# API Request Flow

```text
Client
  │
  ▼
FastAPI Endpoint
  │
  ▼
Pydantic Validation
  │
  ▼
CRUD / SQLAlchemy
  │
  ▼
MySQL Database
  │
  ▼
Response Schema
  │
  ▼
JSON Response
```

---

# Work Item Request Flow

```text
Create Work Item
       │
       ▼
Validate request
       │
       ▼
Validate title
       │
       ▼
Validate employee_id
       │
       ├── Invalid ──► 422 Unprocessable Entity
       │
       ▼
Check employee exists
       │
       ├── No ──► 404 Not Found
       │
       ▼
Create Work Item
       │
       ▼
Store employee_id as Foreign Key
       │
       ▼
Load assigned employee
       │
       ▼
Return Work Item + Employee Details
```

---

# Requirements

The project dependencies are listed in:

```text
requirements.txt
```

Install them using:

```bash
pip install -r requirements.txt
```

Important packages include:

```text
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
pydantic
email-validator
```

---

# Security

Sensitive configuration values such as database passwords should be stored in `.env`.

The `.env` file should not be committed to the repository.

Example `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# Swagger Screenshots

The following screenshots document the API testing performed through Swagger UI.

## Employee API

### Health of API

![Health of API Swagger](screenshots/gethealth.jpg)

### View Employee

![Get Employees](screenshots/getempresbod.jpg)

### Update Employee

![Update Employee](screenshots/updempbod.jpg)

### Delete Employee

![Delete Employee](screenshots/delempresbod.jpg)

### Search and Filtering

#### Employee Search by Name

![Employee Search by name](screenshots/namesearch.jpg)

#### Employee Search by Department

![Employee Search by department](screenshots/searchbydept.jpg)

### Work Mode Validation

![Work Mode Validation](screenshots/workmodevalidator.jpg)

---

# Work Item API Screenshots

## Create / View Work Items

![Get Work Items](screenshots/post_work_items.jpg)

## Retrieve Work Item by ID

![Get work item by ID](screenshots/work_item_by_id.jpg)

## Search Using Work Item Title

![Search by work item title](screenshots/search_by_work_item_title.jpg)

## Invalid Status and Priority Values

![Testing invalid status and priority](screenshots/invalid_status\&priority.jpg)

## Work Item Assigned to Non-existing Employee

![Assigning work item to non-existing employee](screenshots/nonexisting_emp_id.jpg)

## Work Item Pagination

![Testing pagination using limit and offset](screenshots/pagination_by_limit\&offset.jpg)

## Combined Filters

![Testing multiple filters - employee, status, priority, limit and offset](screenshots/filterbyemp_status_priority.jpg)

## Delete Work Item

![Delete Work Item](screenshots/delete_work_item.jpg)

## Blank Title Validation

![Testing blank title validation in Work Item](screenshots/blanktitle.jpg)

## Assign Work Item to Another Employee

![Updating a work item and assigning it to another employee](screenshots/assign_to_another_employee.jpg)

---

# Task 4 Requirements Mapping

| Requirement                  | Implementation                         |
| ---------------------------- | -------------------------------------- |
| `work_items` table           | Added                                  |
| Auto-generated ID            | SQLAlchemy primary key                 |
| Required title               | Pydantic validation                    |
| Blank title rejection        | Validation                             |
| Maximum 255-character title  | Pydantic validation                    |
| Optional description         | Supported                              |
| Employee assignment          | `employee_id`                          |
| Positive employee ID         | `employee_id > 0` validation           |
| Employee foreign key         | `ForeignKey("employees.id")`           |
| SQLAlchemy relationship      | Employee ↔ WorkItem                    |
| Status values                | TODO, IN_PROGRESS, COMPLETED           |
| Priority values              | LOW, MEDIUM, HIGH                      |
| Default status               | TODO                                   |
| Default priority             | MEDIUM                                 |
| Optional due date            | Supported                              |
| Auto-generated created time  | SQLAlchemy timestamp                   |
| Create API                   | `POST /work-items`                     |
| List API                     | `GET /work-items`                      |
| Get by ID                    | `GET /work-items/{work_item_id}`       |
| Update/reassign              | `PUT /work-items/{work_item_id}`       |
| Delete                       | `DELETE /work-items/{work_item_id}`    |
| Search                       | Partial, case-insensitive title search |
| Employee filter              | Supported                              |
| Status filter                | Supported                              |
| Priority filter              | Supported                              |
| Combined filters             | Supported                              |
| Pagination                   | `limit` and `offset`                   |
| Ascending ID order           | Supported                              |
| Total before pagination      | Supported                              |
| Employee details in response | `employee` relationship                |
| Existing Employee APIs       | Preserved                              |

---

# Future Improvements

Possible future enhancements include:

* JWT authentication
* Role-based access control
* Advanced employee filtering
* Sorting support
* Automated testing with Pytest
* Docker support
* Production deployment
* API logging
* Database migrations using Alembic
* More advanced work item sorting and reporting

---

# Author

**Devanand**

Employee Management API developed as part of backend development training using FastAPI, Python, MySQL, and SQLAlchemy.

---

# License

This project is created for learning and development purposes.
