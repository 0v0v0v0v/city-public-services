from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.db.base import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    summary = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    published_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(50), default="published")
