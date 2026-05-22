from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import admin_user, category, news, point  # noqa: F401
from app.seed.data import seed_data


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
