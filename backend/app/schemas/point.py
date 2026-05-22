from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.category import CategoryRead


class PointBase(BaseModel):
    name: str
    category_id: int
    address: str
    opening_hours: str | None = None
    description: str
    service_content: str | None = None
    target_people: str | None = None
    image_url: str | None = None
    is_featured: bool = False
    status: str = "published"


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
