from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    district = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    address = Column(String(255), nullable=False)
    landmark = Column(String(255), nullable=True)
    navigation_notes = Column(Text, nullable=True)
    opening_hours = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    service_content = Column(Text, nullable=True)
    target_people = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    is_featured = Column(Boolean, default=False)
    status = Column(String(50), default="published")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    category = relationship("Category", back_populates="points")
