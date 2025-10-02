from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from .database import get_db
from .schemas import HealthResponse, UploadResponse, BatchInsertResponse, BatchInsertRequest
from .crud import (
    batch_create_departments, batch_create_jobs, batch_create_employees,
    get_department_by_name, get_job_by_name_and_department
)
from .utils import parse_csv_content, get_table_validator, validate_batch_data

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok")


@router.post("/upload-csv", response_model=UploadResponse)
async def upload_csv(
    table: str = Query(..., description="Table name (departments, jobs, employees)"),
    file: UploadFile = File(..., description="CSV file to upload"),
    db: Session = Depends(get_db)
):
    """Upload and process CSV file"""
    
    # Validate table name
    valid_tables = ['departments', 'jobs', 'employees', 'hired_employees']
    if table not in valid_tables:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid table name. Must be one of: {valid_tables}"
        )
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read file content
        content = await file.read()
        logger.info(f"File content length: {len(content)}")
        
        # Parse CSV
        df = parse_csv_content(content)
        logger.info(f"Parsed DataFrame: {df.shape}")
        
        # Get validator for the table
        validator = get_table_validator(table)
        validated_data = validator(df)
        logger.info(f"Validated data count: {len(validated_data)}")
        
        if not validated_data:
            raise HTTPException(status_code=400, detail="No valid data found in CSV")
        
        # Insert data based on table
        records_inserted = 0
        if table == 'departments':
            records_inserted = batch_create_departments(db, validated_data)
        elif table == 'jobs':
            records_inserted = batch_create_jobs(db, validated_data)
        elif table in ['employees', 'hired_employees']:
            records_inserted = batch_create_employees(db, validated_data)
        
        return UploadResponse(
            message=f"Successfully uploaded {records_inserted} records to {table}",
            records_inserted=records_inserted
        )
        
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing CSV: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/batch-insert", response_model=BatchInsertResponse)
async def batch_insert(
    table: str = Query(..., description="Table name (departments, jobs, employees)"),
    request: BatchInsertRequest = ...,
    db: Session = Depends(get_db)
):
    """Batch insert records (1-1000 records)"""
    
    # Validate table name
    valid_tables = ['departments', 'jobs', 'employees', 'hired_employees']
    if table not in valid_tables:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid table name. Must be one of: {valid_tables}"
        )
    
    try:
        # Validate batch data
        validated_data = validate_batch_data(request.data, table)
        
        if not validated_data:
            raise HTTPException(status_code=400, detail="No valid data provided")
        
        # Insert data based on table
        records_inserted = 0
        if table == 'departments':
            records_inserted = batch_create_departments(db, validated_data)
        elif table == 'jobs':
            records_inserted = batch_create_jobs(db, validated_data)
        elif table in ['employees', 'hired_employees']:
            records_inserted = batch_create_employees(db, validated_data)
        
        return BatchInsertResponse(
            message=f"Successfully inserted {records_inserted} records into {table}",
            records_inserted=records_inserted
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in batch insert: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
