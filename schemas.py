from pydantic import BaseModel, Field
from typing import List, Optional

class AgentCreate(BaseModel):
    name: str = Field(..., example="DocParser")
    description: str = Field(..., example="Extracts structured data from PDFs")
    endpoint: str = Field(..., example="https://api.example.com/parse")

class Agent(AgentCreate):
    id: str
    tags: List[str] = []

class UsageLog(BaseModel):
    caller: str
    target: str
    units: int
    request_id: str

class UsageSummary(BaseModel):
    target: str
    total_units: int
