from sqlalchemy import inspect, text

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import admin_user, category, point  # noqa: F401
from app.seed.data import seed_data


def ensure_point_columns() -> None:
    inspector = inspect(engine)
    if "points" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("points")}
    missing_columns = {
        "district": "ALTER TABLE points ADD COLUMN district VARCHAR(100)",
        "street": "ALTER TABLE points ADD COLUMN street VARCHAR(100)",
        "landmark": "ALTER TABLE points ADD COLUMN landmark VARCHAR(255)",
        "navigation_notes": "ALTER TABLE points ADD COLUMN navigation_notes TEXT",
    }

    with engine.begin() as connection:
        for column_name, statement in missing_columns.items():
            if column_name not in existing_columns:
                connection.execute(text(statement))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_point_columns()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()
