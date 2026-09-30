from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.sql import func

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

    __table_args__ = (
        UniqueConstraint(
            "email",
            name="uq_employee_email"
        ),
    )