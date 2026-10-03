from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(255),
        nullable=False,
        unique=True
    )

    department = Column(
        String(50),
        nullable=False
    )

    primary_skill = Column(
        String(50),
        nullable=False
    )

    location = Column(
        String(50),
        nullable=False
    )

    work_mode = Column(
        String(10),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Task 4 relationship
    work_items = relationship(
        "WorkItem",
        back_populates="employee"
    )

    __table_args__ = (
        UniqueConstraint(
            "email",
            name="uq_employee_email"
        ),
    )


class WorkItem(Base):

    __tablename__ = "work_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String(1000),
        nullable=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="TODO"
    )

    priority = Column(
        String(20),
        nullable=False,
        default="MEDIUM"
    )

    due_date = Column(
        Date,
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # Relationship back to Employee
    employee = relationship(
        "Employee",
        back_populates="work_items"
    )