from datetime import date

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.database import Base
from app.models import Application


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    Base.metadata.drop_all(engine)


def test_new_application_defaults_to_applied(session):
    application =  Application(
        company="Acme",
        role="Junior Developer",
        applied_on=date(2026, 10, 1)
    )
    session.add(application)
    session.commit()

    saved = session.scalars(select(Application)).one()

    assert saved.id is not None
    assert saved.company == "Acme"
    assert saved.status == "applied"