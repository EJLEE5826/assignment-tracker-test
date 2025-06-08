from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from datetime import datetime
from models import Assignment, AssignmentCreate
import uvicorn
import os

app = FastAPI(title="Assignment Tracker API", version="1.0.0")

# CORS 설정
# 환경에 따른 허용 도메인 설정
if os.getenv("ENVIRONMENT") == "production":
    origins = [
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "https://assignment-tracker-test.vercel.app") # Change to your production frontend URL
    ]
else:
    origins = [
        "http://localhost:3000",
        "http://localhost:5173", 
        "http://localhost:5174",
        "*"  # 개발 환경에서는 모든 도메인 허용
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 메모리 저장소 (실제 프로덕션에서는 데이터베이스 사용)
assignments_db: Dict[int, dict] = {}
next_id = 1

@app.get("/")
async def root():
    return {"message": "Assignment Tracker API"}

@app.post("/assignments/", response_model=Assignment)
async def create_assignment(assignment: AssignmentCreate):
    global next_id
    
    assignment_dict = {
        "id": next_id,
        "title": assignment.title,
        "description": assignment.description,
        "dueDate": assignment.dueDate,
        "completed": False,
        "createdAt": datetime.now()
    }
    
    assignments_db[next_id] = assignment_dict
    next_id += 1
    
    return Assignment(**assignment_dict)

@app.get("/assignments/", response_model=List[Assignment])
async def get_assignments():
    return [Assignment(**assignment) for assignment in assignments_db.values()]

@app.patch("/assignments/{assignment_id}/complete", response_model=Assignment)
async def complete_assignment(assignment_id: int):
    if assignment_id not in assignments_db:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    assignments_db[assignment_id]["completed"] = True
    return Assignment(**assignments_db[assignment_id])

@app.delete("/assignments/{assignment_id}")
async def delete_assignment(assignment_id: int):
    if assignment_id not in assignments_db:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    del assignments_db[assignment_id]
    return {"message": "Assignment deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
