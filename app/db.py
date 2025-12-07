from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import DB_URL
from .models import Base

# create_engine vytvoří objekt pro komunikaci s databází
engine = create_engine(DB_URL)

# SessionLocal = továrna na session objekty
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    """
    Vytvoří tabulky v databázi podle SQLAlchemy modelů.
    Zavoláme ji jednou na začátku programu.
    """
    Base.metadata.create_all(bind=engine)
