import pandas as pd
import io
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def parse_csv_content(csv_content: bytes) -> pd.DataFrame:
    """Parse CSV content from bytes to pandas DataFrame"""
    try:
        csv_string = csv_content.decode('utf-8')
        # Always parse without headers first, then auto-detect format
        df = pd.read_csv(io.StringIO(csv_string), header=None, sep=',')
        # Auto-detect format based on number of columns
        if len(df.columns) == 2:
            # Check if it's departments or jobs by looking at first row
            first_row = df.iloc[0, 1] if len(df) > 0 else ""
            if "Supply Chain" in str(first_row) or "Maintenance" in str(first_row):
                df.columns = ['id', 'department']
            elif "Recruiter" in str(first_row) or "Manager" in str(first_row):
                df.columns = ['id', 'job']
            else:
                df.columns = ['id', 'name']  # fallback
        elif len(df.columns) == 4:
            df.columns = ['id', 'name', 'datetime', 'department_id']
        elif len(df.columns) == 5:
            df.columns = ['id', 'name', 'datetime', 'department_id', 'job_id']
        return df
    except Exception as e:
        logger.error(f"Error parsing CSV: {e}")
        raise ValueError(f"Invalid CSV format: {e}")


def validate_departments_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Validate and prepare departments data from DataFrame"""
    # Handle both formats: with/without id column
    if 'id' in df.columns and 'department' in df.columns:
        # Format: id,department
        required_columns = ['id', 'department']
    else:
        # Format: department only
        required_columns = ['department']
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Prepare data
    departments = []
    for _, row in df.iterrows():
        if pd.isna(row['department']) or str(row['department']).strip() == '':
            continue
            
        departments.append({
            'department': str(row['department']).strip()
        })
    
    return departments


def validate_jobs_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Validate and prepare jobs data from DataFrame"""
    # Handle both formats: with/without id column
    if 'id' in df.columns and 'job' in df.columns:
        # Format: id,job (no department_id in CSV)
        required_columns = ['id', 'job']
    else:
        # Format: job,department_id
        required_columns = ['job', 'department_id']
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Prepare data
    jobs = []
    for _, row in df.iterrows():
        if pd.isna(row['job']) or str(row['job']).strip() == '':
            continue
        
        # Handle different formats
        if 'department_id' in df.columns:
            if pd.isna(row['department_id']):
                continue
            jobs.append({
                'job': str(row['job']).strip(),
                'department_id': int(row['department_id'])
            })
        else:
            # For format without department_id, we'll need to handle this differently
            # This might require additional logic or a default department
            jobs.append({
                'job': str(row['job']).strip(),
                'department_id': 1  # Default department - this might need adjustment
            })
    
    return jobs


def validate_employees_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Validate and prepare employees data from DataFrame"""
    # Handle both formats: with/without id column
    if 'id' in df.columns:
        # Format: id,name,datetime,department_id,job_id
        required_columns = ['id', 'name', 'datetime', 'department_id', 'job_id']
    else:
        # Format: name,datetime,department_id,job_id
        required_columns = ['name', 'datetime', 'department_id', 'job_id']
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Prepare data
    employees = []
    for _, row in df.iterrows():
        if pd.isna(row['name']) or str(row['name']).strip() == '':
            continue
        if pd.isna(row['datetime']):
            continue
        if pd.isna(row['department_id']) or pd.isna(row['job_id']):
            continue
            
        # Parse datetime
        try:
            if isinstance(row['datetime'], str):
                datetime_obj = pd.to_datetime(row['datetime'])
            else:
                datetime_obj = row['datetime']
        except:
            logger.warning(f"Invalid datetime format for row: {row}")
            continue
            
        employees.append({
            'name': str(row['name']).strip(),
            'datetime': datetime_obj,
            'department_id': int(row['department_id']),
            'job_id': int(row['job_id'])
        })
    
    return employees


def get_table_validator(table_name: str):
    """Get the appropriate validator function for a table"""
    validators = {
        'departments': validate_departments_data,
        'jobs': validate_jobs_data,
        'employees': validate_employees_data,
        'hired_employees': validate_employees_data  # Same validation as employees
    }
    
    if table_name not in validators:
        raise ValueError(f"Unsupported table: {table_name}. Supported tables: {list(validators.keys())}")
    
    return validators[table_name]


def validate_batch_data(data: List[Dict[str, Any]], table_name: str) -> List[Dict[str, Any]]:
    """Validate batch insert data for a specific table"""
    if not data:
        raise ValueError("Empty data list")
    
    if len(data) > 1000:
        raise ValueError("Batch size cannot exceed 1000 records")
    
    # Convert to DataFrame for validation
    df = pd.DataFrame(data)
    
    # Get appropriate validator
    validator = get_table_validator(table_name)
    
    return validator(df)
