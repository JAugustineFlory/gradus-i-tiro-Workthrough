from datetime import date

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "applied"
    applied_on: date


class ApplicationUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    status: str  | None = None
    applied_on: date  | None = None


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    status: str
    applied_on: date