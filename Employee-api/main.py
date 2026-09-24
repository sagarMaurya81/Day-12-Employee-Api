from fastapi import FastAPI

from database.db import Base, engine
from routes.employees import router as employee_router


app = FastAPI(
    title="Employee Management API",
    description="FastAPI Employee CRUD API",
    version="1.0.0"
)


# Create database tables
Base.metadata.create_all(
    bind=engine
)


# Register routes
app.include_router(
    employee_router
)


@app.get("/")
def root():
    return {
        "message": "Employee Management API is running"
    }