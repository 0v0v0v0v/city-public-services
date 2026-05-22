from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from app.api.deps import get_current_admin, get_db
from app.models.category import Category
from app.models.news import News
from app.models.point import Point
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.news import NewsCreate, NewsUpdate
from app.schemas.point import PointCreate, PointUpdate
from app.services.query import paginate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard")
def dashboard(_: object = Depends(get_current_admin), db=Depends(get_db)):
    return {
        "category_count": db.query(Category).count(),
        "point_count": db.query(Point).count(),
        "news_count": db.query(News).count(),
    }


@router.get("/categories")
def admin_list_categories(_: object = Depends(get_current_admin), db=Depends(get_db)):
    return db.query(Category).order_by(Category.sort_order.asc(), Category.id.asc()).all()


@router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, _: object = Depends(get_current_admin), db=Depends(get_db)):
    exists = db.query(Category).filter(
        (Category.name == payload.name) | (Category.slug == payload.slug)
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="分类名称或 slug 已存在。")
    item = Category(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    _: object = Depends(get_current_admin),
    db=Depends(get_db),
):
    item = db.query(Category).filter(Category.id == category_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="分类不存在。")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int, _: object = Depends(get_current_admin), db=Depends(get_db)
):
    item = db.query(Category).filter(Category.id == category_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="分类不存在。")
    db.delete(item)
    db.commit()
    return {"message": "分类已删除。"}


@router.get("/points")
def admin_list_points(
    page: int = 1, page_size: int = 20, _: object = Depends(get_current_admin), db=Depends(get_db)
):
    query = db.query(Point).options(joinedload(Point.category)).order_by(Point.updated_at.desc())
    items, total = paginate(query, page, min(page_size, 100))
    return {"items": items, "total": total, "page": page, "page_size": min(page_size, 100)}


@router.post("/points", status_code=status.HTTP_201_CREATED)
def create_point(payload: PointCreate, _: object = Depends(get_current_admin), db=Depends(get_db)):
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="分类不存在。")
    item = Point(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return (
        db.query(Point)
        .options(joinedload(Point.category))
        .filter(Point.id == item.id)
        .first()
    )


@router.put("/points/{point_id}")
def update_point(
    point_id: int, payload: PointUpdate, _: object = Depends(get_current_admin), db=Depends(get_db)
):
    item = db.query(Point).filter(Point.id == point_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="点位不存在。")
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="分类不存在。")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return (
        db.query(Point)
        .options(joinedload(Point.category))
        .filter(Point.id == item.id)
        .first()
    )


@router.delete("/points/{point_id}")
def delete_point(point_id: int, _: object = Depends(get_current_admin), db=Depends(get_db)):
    item = db.query(Point).filter(Point.id == point_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="点位不存在。")
    db.delete(item)
    db.commit()
    return {"message": "点位已删除。"}


@router.get("/news")
def admin_list_news(
    page: int = 1, page_size: int = 20, _: object = Depends(get_current_admin), db=Depends(get_db)
):
    query = db.query(News).order_by(News.published_at.desc())
    items, total = paginate(query, page, min(page_size, 100))
    return {"items": items, "total": total, "page": page, "page_size": min(page_size, 100)}


@router.post("/news", status_code=status.HTTP_201_CREATED)
def create_news(payload: NewsCreate, _: object = Depends(get_current_admin), db=Depends(get_db)):
    item = News(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/news/{news_id}")
def update_news(
    news_id: int, payload: NewsUpdate, _: object = Depends(get_current_admin), db=Depends(get_db)
):
    item = db.query(News).filter(News.id == news_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="资讯不存在。")
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/news/{news_id}")
def delete_news(news_id: int, _: object = Depends(get_current_admin), db=Depends(get_db)):
    item = db.query(News).filter(News.id == news_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="资讯不存在。")
    db.delete(item)
    db.commit()
    return {"message": "资讯已删除。"}
