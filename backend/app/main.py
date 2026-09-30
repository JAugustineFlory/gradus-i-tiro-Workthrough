from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
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

@app.get(
    "/applications",
    response_model=list[schemas.ApplicationRead],
)
def list_applications(db: Annotated[Session, Depends(get_db)]):
    query = select(models.Application).order_by(models.Application.id)
    return db.scalars(query).all()