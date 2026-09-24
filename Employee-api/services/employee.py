from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeePartialUpdate
)

from models.employee import Employee


# =========================================================
# Check unique email and phone
# =========================================================

def validate_unique_employee(
    db: Session,
    email: str | None = None,
    phone_number: str | None = None,
    exclude_employee_id: int | None = None
):

    # -------------------------------
    # Check Email
    # -------------------------------

    if email is not None:

        query = db.query(Employee).filter(
            Employee.email == email
        )

        if exclude_employee_id is not None:
            query = query.filter(
                Employee.employee_id != exclude_employee_id
            )

        existing_employee = query.first()

        if existing_employee:
            raise ValueError(
                "Email already exists"
            )

    # -------------------------------
    # Check Phone
    # -------------------------------

    if phone_number is not None:

        query = db.query(Employee).filter(
            Employee.phone_number == phone_number
        )

        if exclude_employee_id is not None:
            query = query.filter(
                Employee.employee_id != exclude_employee_id
            )

        existing_employee = query.first()

        if existing_employee:
            raise ValueError(
                "Phone number already exists"
            )


# =========================================================
# CREATE
# =========================================================

def create_employee(
    db: Session,
    employee_data: EmployeeCreate
) -> Employee:

    email = str(employee_data.email)

    # Check duplicate email and phone
    validate_unique_employee(
        db=db,
        email=email,
        phone_number=employee_data.phone_number
    )

    employee = Employee(
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=email,
        phone_number=employee_data.phone_number
    )

    try:

        db.add(employee)
        db.commit()
        db.refresh(employee)

    except IntegrityError:

        db.rollback()

        raise ValueError(
            "Email or phone number already exists"
        )

    except SQLAlchemyError:

        db.rollback()

        raise ValueError(
            "Database error while creating employee"
        )

    return employee


# =========================================================
# GET ALL
# =========================================================

def get_employees(
    db: Session
) -> list[Employee]:

    try:

        return (
            db.query(Employee)
            .order_by(Employee.employee_id)
            .all()
        )

    except SQLAlchemyError:

        raise ValueError(
            "Database error while fetching employees"
        )


# =========================================================
# GET ONE
# =========================================================

def get_employee(
    db: Session,
    employee_id: int
) -> Employee | None:

    try:

        return (
            db.query(Employee)
            .filter(
                Employee.employee_id == employee_id
            )
            .first()
        )

    except SQLAlchemyError:

        raise ValueError(
            "Database error while fetching employee"
        )


# =========================================================
# FULL UPDATE
# =========================================================

def update_employee(
    db: Session,
    employee: Employee,
    employee_data: EmployeeUpdate
) -> Employee:

    email = str(employee_data.email)

    # Check duplicate email and phone
    # Ignore current employee
    validate_unique_employee(
        db=db,
        email=email,
        phone_number=employee_data.phone_number,
        exclude_employee_id=employee.employee_id
    )

    employee.first_name = employee_data.first_name
    employee.last_name = employee_data.last_name
    employee.email = email
    employee.phone_number = employee_data.phone_number

    try:

        db.commit()
        db.refresh(employee)

    except IntegrityError:

        db.rollback()

        raise ValueError(
            "Email or phone number already exists"
        )

    except SQLAlchemyError:

        db.rollback()

        raise ValueError(
            "Database error while updating employee"
        )

    return employee


# =========================================================
# DELETE
# =========================================================

def delete_employee(
    db: Session,
    employee: Employee
) -> None:

    try:

        db.delete(employee)
        db.commit()

    except IntegrityError:

        db.rollback()

        raise ValueError(
            "Employee cannot be deleted because related records exist"
        )

    except SQLAlchemyError:

        db.rollback()

        raise ValueError(
            "Database error while deleting employee"
        )


# =========================================================
# PARTIAL UPDATE
# =========================================================

def update_employee_partial(
    db: Session,
    employee: Employee,
    employee_data: EmployeePartialUpdate
) -> Employee:

    # Get only fields provided by client
    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    # -----------------------------------------------------
    # Check email
    # -----------------------------------------------------

    if "email" in update_data:

        email = update_data["email"]

        if email is not None:

            email = str(email)

            validate_unique_employee(
                db=db,
                email=email,
                exclude_employee_id=employee.employee_id
            )

            update_data["email"] = email

    # -----------------------------------------------------
    # Check phone
    # -----------------------------------------------------

    if "phone_number" in update_data:

        phone_number = update_data["phone_number"]

        if phone_number is not None:

            validate_unique_employee(
                db=db,
                phone_number=phone_number,
                exclude_employee_id=employee.employee_id
            )

    # -----------------------------------------------------
    # Update provided fields only
    # -----------------------------------------------------

    for field, value in update_data.items():

        setattr(
            employee,
            field,
            value
        )

    try:

        db.commit()
        db.refresh(employee)

    except IntegrityError:

        db.rollback()

        raise ValueError(
            "Email or phone number already exists"
        )

    except SQLAlchemyError:

        db.rollback()

        raise ValueError(
            "Database error while partially updating employee"
        )

    return employee