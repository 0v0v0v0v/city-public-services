from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    icon = Column(String(255), nullable=True)
    cover_image = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0)
    description = Column(Text, nullable=True)

    points = relationship("Point", back_populates="category", cascade="all, delete")
