import pytest
from sqlalchemy.orm import Session 
#Session acts as a workspace for all 
# ORM objects and database interactions. It maintains an "Identity Map"
# which ensures each object with a primary key exists only once in memory

from app.database import get_db


@pytest.mark.auth
def test_get_db_yields_a_session_and_closes_it():
  generator = get_db()

  db = next(generator)

  assert isinstance(db, Session)
  generator.close()