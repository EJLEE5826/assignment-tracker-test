from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    dueDate: Optional[datetime] = None

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    completed: bool = False
    createdAt: datetime
    
    model_config = ConfigDict(from_attributes=True)
