from pydantic import BaseModel

from app.schemas.category import CategoryRead
from app.schemas.point import PointRead


class HomeResponse(BaseModel):
    featured_points: list[PointRead]
    categories: list[CategoryRead]
