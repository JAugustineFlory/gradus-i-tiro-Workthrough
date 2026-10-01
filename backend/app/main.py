from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

app = FastAPI(title="Tiro Job Tracker")


def find_application_or_404(
  db: Session,
  application_id: int,
) -> models.Application:
  application = db.get(models.Application, application_id)
  if application is None:
    raise HTTPException(
      status_code=404,
      detail="Application not found",
    )
  return application


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


@app.get("/applications/{application_id}",
    response_model=schemas.ApplicationRead,
)
def get_application(
    application_id: int,
    db: Annotated[Session, Depends(get_db)],
):
  return find_application_or_404(db, application_id)



@app.patch(
    "/applications/{application_id}",
    response_model=schemas.ApplicationRead,
)
def update_application(
    application_id: int,
    payload: schemas.ApplicationUpdate,
    db: Annotated[Session, Depends(get_db)],
):
  application = find_application_or_404(db, application_id)
  changes = payload.model_dump(exclude_unset=True)
  for field, value in changes.items():
    setattr(application, field, value)
  db.commit()
  db.refresh(application)
  return application


@app.delete(
  "/applications/{application_id}",
  status_code=204,
)
def delete_application(
  application_id: int,
  db: Annotated[Session, Depends(get_db)],
):
  application = find_application_or_404(db, application_id)
  db.delete(application)
  db.commit()