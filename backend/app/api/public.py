from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import joinedload

from app.api.deps import get_db
from app.models.category import Category
from app.models.point import Point
from app.schemas.home import HomeResponse
from app.services.query import apply_point_filters, paginate

router = APIRouter()


@router.get("/categories")
def list_categories(db=Depends(get_db)):
    return db.query(Category).order_by(Category.sort_order.asc(), Category.id.asc()).all()


@router.get("/points")
def list_points(
    keyword: str | None = None,
    category_id: int | None = None,
    is_featured: bool | None = None,
    page: int = 1,
    page_size: int = 10,
    db=Depends(get_db),
):
    query = (
        db.query(Point)
        .options(joinedload(Point.category))
        .filter(Point.status == "published")
        .order_by(Point.is_featured.desc(), Point.updated_at.desc())
    )
    query = apply_point_filters(query, keyword, category_id, is_featured)
    items, total = paginate(query, page, min(page_size, 50))
    return {"items": items, "total": total, "page": page, "page_size": min(page_size, 50)}


@router.get("/points/{point_id}")
def get_point(point_id: int, db=Depends(get_db)):
    point = (
        db.query(Point)
        .options(joinedload(Point.category))
        .filter(Point.id == point_id, Point.status == "published")
        .first()
    )
    if not point:
        raise HTTPException(status_code=404, detail="未找到该便民点位。")
    return point


@router.get("/home", response_model=HomeResponse)
def get_home(db=Depends(get_db)):
    featured_points = (
        db.query(Point)
        .options(joinedload(Point.category))
        .filter(Point.status == "published", Point.is_featured.is_(True))
        .order_by(Point.updated_at.desc())
        .limit(6)
        .all()
    )
    categories = db.query(Category).order_by(Category.sort_order.asc()).limit(8).all()
    return HomeResponse(featured_points=featured_points, categories=categories)
