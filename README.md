# Employee Management API

A simple **Employee Management REST API** built using **FastAPI, SQLAlchemy, Pydantic, and PostgreSQL**.

## Features

- Create employee
- Get all employees
- Get employee by ID
- Full update using PUT
- Partial update using PATCH
- Delete employee
- Pydantic request validation
- Unique email and phone validation
- SQLAlchemy database operations
- Swagger API documentation
- Error handling

## Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **PostgreSQL**
- **Uvicorn**
- **psycopg2**

## Project Structure

```text
Employee-api/
│
├── main.py
│
├── database/
│   └── db.py
│
├── models/
│   └── employee.py
│
├── schemas/
│   └── employee.py
│
├── services/
│   └── employee.py
│
└── routes/
    └── employee.py
```

## Installation

Clone the project:

```bash
git clone <your-repository-url>
cd Employee-api
```

Create virtual environment:

```bash
python -m venv venv
```

Activate it on Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic[email]
```

## Database Configuration

Create a PostgreSQL database:

```sql
CREATE DATABASE employee_db;
```

Update the database URL in `database/db.py`:

```python
DATABASE_URL = (
    "postgresql+psycopg2://postgres:password@localhost:5432/employee_db"
)
```

Change `postgres` and `password` according to your PostgreSQL setup.

## Run the Project

```bash
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/employees/create` | Create employee |
| GET | `/employees/employee-list` | Get all employees |
| GET | `/employees/{employee_id}` | Get employee by ID |
| PUT | `/employees/{employee_id}` | Full update |
| PATCH | `/employees/update/{employee_id}` | Partial update |
| DELETE | `/employees/{employee_id}` | Delete employee |

## Example Request

### Create Employee

```json
{
  "first_name": "Sagar",
  "last_name": "Maurya",
  "email": "sagar@gmail.com",
  "phone_number": "9876543210"
}
```

### Partial Update

```json
{
  "email": "newemail@gmail.com"
}
```

## Validation

- `first_name`: 3–50 characters
- `last_name`: optional, 2–50 characters
- `email`: valid email format
- `phone_number`: optional, exactly 10 digits
- `employee_id`: greater than 0
- Email and phone number must be unique in the database

## HTTP Status Codes

```text
200 → Success
201 → Employee created
204 → Employee deleted
404 → Employee not found
409 → Duplicate/conflict data
422 → Validation error
500 → Internal server error
```

## API Flow

```text
Client
   ↓
FastAPI Route
   ↓
Pydantic Validation
   ↓
Service Layer
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
Response Model
   ↓
Client
```

## License

This project is for learning and practice purposes.