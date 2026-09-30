from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

app = FastAPI(title="Tiro Job Tracker")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post(
    "/applications",
    response_model=schemas.ApplicationRead,
    status_code=201,
)
def create_application(
    payload: schemas.ApplicationCreate,
    db: Annotated[Session, Depends(get_db)],
):
    application = models.Application(**payload.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application
