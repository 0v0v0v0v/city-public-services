from sqlalchemy import func, or_
from sqlalchemy.orm import Query

from app.models.point import Point


def apply_point_filters(
    query: Query,
    keyword: str | None = None,
    category_id: int | None = None,
    is_featured: bool | None = None,
) -> Query:
    if keyword:
        pattern = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Point.name.ilike(pattern),
                Point.address.ilike(pattern),
                Point.description.ilike(pattern),
                Point.service_content.ilike(pattern),
            )
        )
    if category_id:
        query = query.filter(Point.category_id == category_id)
    if is_featured is not None:
        query = query.filter(Point.is_featured == is_featured)
    return query


def paginate(query: Query, page: int, page_size: int) -> tuple[list, int]:
    total = query.with_entities(func.count()).scalar() or 0
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total
