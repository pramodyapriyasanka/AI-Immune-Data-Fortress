from pydantic import BaseModel
from typing import Optional

class AuditResult(BaseModel):
    status: str  # PASS or FAIL
    reason: str
    confidence_score: float

class DataRecord(BaseModel):
    user_id: int
    user_name: str
    age: int
    location: str
    timestamp: str