from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# Department schemas
class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100)


class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Job schemas
class JobBase(BaseModel):
    name: str = Field(..., max_length=100)
    department_id: int


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Employee schemas
class EmployeeBase(BaseModel):
    name: str = Field(..., max_length=100)
    datetime: datetime
    department_id: int
    job_id: int


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Batch insert schemas
class BatchInsertRequest(BaseModel):
    data: List[dict] = Field(..., min_items=1, max_items=1000)


# Response schemas
class HealthResponse(BaseModel):
    status: str


class UploadResponse(BaseModel):
    message: str
    records_inserted: int


class BatchInsertResponse(BaseModel):
    message: str
    records_inserted: int
