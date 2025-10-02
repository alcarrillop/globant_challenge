from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any
from . import models, schemas


def create_department(db: Session, department: schemas.DepartmentCreate) -> models.Department:
    """Create a new department"""
    db_department = models.Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def create_job(db: Session, job: schemas.JobCreate) -> models.Job:
    """Create a new job"""
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def create_employee(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
    """Create a new employee"""
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def batch_create_departments(db: Session, departments: List[Dict[str, Any]]) -> int:
    """Create multiple departments in batch"""
    try:
        db_departments = [models.Department(**dept) for dept in departments]
        db.add_all(db_departments)
        db.commit()
        return len(db_departments)
    except IntegrityError:
        db.rollback()
        raise


def batch_create_jobs(db: Session, jobs: List[Dict[str, Any]]) -> int:
    """Create multiple jobs in batch"""
    try:
        db_jobs = [models.Job(**job) for job in jobs]
        db.add_all(db_jobs)
        db.commit()
        return len(db_jobs)
    except IntegrityError:
        db.rollback()
        raise


def batch_create_employees(db: Session, employees: List[Dict[str, Any]]) -> int:
    """Create multiple employees in batch"""
    try:
        db_employees = [models.Employee(**emp) for emp in employees]
        db.add_all(db_employees)
        db.commit()
        return len(db_employees)
    except IntegrityError:
        db.rollback()
        raise


def get_department_by_name(db: Session, department: str) -> models.Department:
    """Get department by name"""
    return db.query(models.Department).filter(models.Department.department == department).first()


def get_job_by_name_and_department(db: Session, job: str, department_id: int) -> models.Job:
    """Get job by name and department"""
    return db.query(models.Job).filter(
        models.Job.job == job,
        models.Job.department_id == department_id
    ).first()


def get_department_by_id(db: Session, department_id: int) -> models.Department:
    """Get department by ID"""
    return db.query(models.Department).filter(models.Department.id == department_id).first()


def get_job_by_id(db: Session, job_id: int) -> models.Job:
    """Get job by ID"""
    return db.query(models.Job).filter(models.Job.id == job_id).first()
