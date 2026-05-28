from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryRead

PointStatus = Literal["draft", "published"]


class PointBase(BaseModel):
    name: str
    category_id: int
    district: str | None = None
    street: str | None = None
    address: str
    landmark: str | None = None
    navigation_notes: str | None = None
    opening_hours: str | None = None
    description: str
    service_content: str | None = None
    target_people: str | None = None
    image_url: str | None = None
    is_featured: bool = False
    status: PointStatus = "draft"


class PointCreate(PointBase):
    pass


class PointUpdate(PointBase):
    pass


class PointRead(PointBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryRead
    model_config = ConfigDict(from_attributes=True)
