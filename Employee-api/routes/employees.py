from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status
)

from sqlalchemy.orm import Session

from database.db import get_db

from schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeePartialUpdate
)

from services.employee import (
    create_employee,
    delete_employee,
    get_employee,
    get_employees,
    update_employee,
    update_employee_partial
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# =========================================================
# CREATE EMPLOYEE
# =========================================================

@router.post(
    "/create",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create employee"
)
def create_employee_endpoint(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_employee(
            db,
            employee_data
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# =========================================================
# GET ALL EMPLOYEES
# =========================================================

@router.get(
    "/employee-list",
    response_model=list[EmployeeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all employees"
)
def get_employees_endpoint(
    db: Session = Depends(get_db)
):

    try:

        return get_employees(db)

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch employees"
        )


# =========================================================
# GET EMPLOYEE BY ID
# =========================================================

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get employee by ID"
)
def get_employee_endpoint(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    ),
    db: Session = Depends(get_db)
):

    try:

        employee = get_employee(
            db,
            employee_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found."
        )

    return employee


# =========================================================
# FULL UPDATE
# =========================================================

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Update employee"
)
def update_employee_endpoint(
    employee_data: EmployeeUpdate,
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID"
    ),
    db: Session = Depends(get_db)
):

    employee = get_employee(
        db,
        employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found."
        )

    try:

        return update_employee(
            db,
            employee,
            employee_data
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update employee"
        )


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee"
)
def delete_employee_endpoint(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID"
    ),
    db: Session = Depends(get_db)
):

    employee = get_employee(
        db,
        employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found."
        )

    try:

        delete_employee(
            db,
            employee
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete employee"
        )

    return None


# =========================================================
# PARTIAL UPDATE
# =========================================================

@router.patch(
    "/update/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Partial update of employee"
)
def partial_update_employee(
    employee_data: EmployeePartialUpdate,
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID"
    ),
    db: Session = Depends(get_db)
):

    employee = get_employee(
        db,
        employee_id
    )

    if employee is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found."
        )

    try:

        return update_employee_partial(
            db,
            employee,
            employee_data
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to partially update employee"
        )