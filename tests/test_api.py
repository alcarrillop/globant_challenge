import pytest
from fastapi.testclient import TestClient
from io import BytesIO
import json


def test_health_endpoint(client: TestClient):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_csv_departments(client: TestClient):
    """Test CSV upload for departments"""
    csv_content = "name\nEngineering\nMarketing"
    csv_file = BytesIO(csv_content.encode())
    
    response = client.post(
        "/upload-csv?table=departments",
        files={"file": ("departments.csv", csv_file, "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["records_inserted"] == 2
    assert "Successfully uploaded" in data["message"]


def test_upload_csv_jobs(client: TestClient):
    """Test CSV upload for jobs"""
    csv_content = "name,department_id\nSoftware Engineer,1\nMarketing Manager,2"
    csv_file = BytesIO(csv_content.encode())
    
    response = client.post(
        "/upload-csv?table=jobs",
        files={"file": ("jobs.csv", csv_file, "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["records_inserted"] == 2
    assert "Successfully uploaded" in data["message"]


def test_upload_csv_employees(client: TestClient):
    """Test CSV upload for employees"""
    csv_content = "name,datetime,department_id,job_id\nJohn Doe,2023-01-15 09:00:00,1,1"
    csv_file = BytesIO(csv_content.encode())
    
    response = client.post(
        "/upload-csv?table=employees",
        files={"file": ("employees.csv", csv_file, "text/csv")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["records_inserted"] == 1
    assert "Successfully uploaded" in data["message"]


def test_upload_csv_invalid_table(client: TestClient):
    """Test CSV upload with invalid table name"""
    csv_content = "name\nTest"
    csv_file = BytesIO(csv_content.encode())
    
    response = client.post(
        "/upload-csv?table=invalid_table",
        files={"file": ("test.csv", csv_file, "text/csv")}
    )
    
    assert response.status_code == 400
    assert "Invalid table name" in response.json()["detail"]


def test_upload_csv_invalid_file_type(client: TestClient):
    """Test CSV upload with invalid file type"""
    content = "This is not a CSV"
    file = BytesIO(content.encode())
    
    response = client.post(
        "/upload-csv?table=departments",
        files={"file": ("test.txt", file, "text/plain")}
    )
    
    assert response.status_code == 400
    assert "File must be a CSV" in response.json()["detail"]


def test_batch_insert_departments(client: TestClient):
    """Test batch insert for departments"""
    data = {
        "data": [
            {"name": "Engineering"},
            {"name": "Marketing"}
        ]
    }
    
    response = client.post(
        "/batch-insert?table=departments",
        json=data
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["records_inserted"] == 2
    assert "Successfully inserted" in response_data["message"]


def test_batch_insert_jobs(client: TestClient):
    """Test batch insert for jobs"""
    data = {
        "data": [
            {"name": "Software Engineer", "department_id": 1},
            {"name": "Marketing Manager", "department_id": 2}
        ]
    }
    
    response = client.post(
        "/batch-insert?table=jobs",
        json=data
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["records_inserted"] == 2
    assert "Successfully inserted" in response_data["message"]


def test_batch_insert_employees(client: TestClient):
    """Test batch insert for employees"""
    data = {
        "data": [
            {
                "name": "John Doe",
                "datetime": "2023-01-15T09:00:00",
                "department_id": 1,
                "job_id": 1
            }
        ]
    }
    
    response = client.post(
        "/batch-insert?table=employees",
        json=data
    )
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["records_inserted"] == 1
    assert "Successfully inserted" in response_data["message"]


def test_batch_insert_invalid_table(client: TestClient):
    """Test batch insert with invalid table name"""
    data = {"data": [{"name": "Test"}]}
    
    response = client.post(
        "/batch-insert?table=invalid_table",
        json=data
    )
    
    assert response.status_code == 400
    assert "Invalid table name" in response.json()["detail"]


def test_batch_insert_empty_data(client: TestClient):
    """Test batch insert with empty data"""
    data = {"data": []}
    
    response = client.post(
        "/batch-insert?table=departments",
        json=data
    )
    
    assert response.status_code == 400
    assert "Empty data list" in response.json()["detail"]


def test_batch_insert_too_many_records(client: TestClient):
    """Test batch insert with too many records"""
    data = {"data": [{"name": f"Department {i}"} for i in range(1001)]}
    
    response = client.post(
        "/batch-insert?table=departments",
        json=data
    )
    
    assert response.status_code == 400
    assert "Batch size cannot exceed 1000 records" in response.json()["detail"]
