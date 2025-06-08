import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment Tracker API"}

def test_create_assignment():
    assignment_data = {
        "title": "Test Assignment",
        "description": "Test Description",
        "dueDate": "2024-12-31T23:59:59"
    }
    
    response = client.post("/assignments/", json=assignment_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == assignment_data["title"]
    assert data["description"] == assignment_data["description"]
    assert data["completed"] == False
    assert "id" in data
    assert "createdAt" in data

def test_get_assignments():
    # 먼저 과제 생성
    assignment_data = {
        "title": "Test Assignment 2",
        "description": "Test Description 2"
    }
    client.post("/assignments/", json=assignment_data)
    
    response = client.get("/assignments/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_complete_assignment():
    # 먼저 과제 생성
    assignment_data = {
        "title": "Test Assignment 3",
        "description": "Test Description 3"
    }
    create_response = client.post("/assignments/", json=assignment_data)
    assignment_id = create_response.json()["id"]
    
    # 과제 완료 처리
    response = client.patch(f"/assignments/{assignment_id}/complete")
    assert response.status_code == 200
    
    data = response.json()
    assert data["completed"] == True

def test_complete_nonexistent_assignment():
    response = client.patch("/assignments/999/complete")
    assert response.status_code == 404
