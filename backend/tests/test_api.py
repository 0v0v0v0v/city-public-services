from fastapi.testclient import TestClient
from uuid import uuid4

from app.db.init_db import init_db  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)
init_db()


def get_token():
    response = client.post(
        "/api/admin/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_public_points_filtering():
    response = client.get("/api/points", params={"keyword": "公园", "is_featured": True})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] >= 1
    assert any("公园" in item["name"] for item in payload["items"])


def test_public_detail_not_found():
    response = client.get("/api/points/999999")
    assert response.status_code == 404


def test_admin_login_failure():
    response = client.post(
        "/api/admin/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_admin_create_and_update_category():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    unique_suffix = uuid4().hex[:8]
    create_response = client.post(
        "/api/admin/categories",
        json={
            "name": f"应急避难场所-{unique_suffix}",
            "slug": f"shelters-{unique_suffix}",
            "icon": "shield",
            "cover_image": "",
            "sort_order": 8,
            "description": "用于临时避难和应急集合的公共空间。",
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    category_id = create_response.json()["id"]

    update_response = client.put(
        f"/api/admin/categories/{category_id}",
        json={
            "name": f"应急避难场所-{unique_suffix}",
            "slug": f"shelters-{unique_suffix}",
            "icon": "shield-check",
            "cover_image": "",
            "sort_order": 9,
            "description": "更新后的说明。",
        },
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["icon"] == "shield-check"


def test_admin_create_point_visible_in_public_search():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    categories = client.get("/api/admin/categories", headers=headers).json()
    category_id = categories[0]["id"]
    create_response = client.post(
        "/api/admin/points",
        json={
            "name": "晨曦公益运动角",
            "category_id": category_id,
            "address": "松风路 18 号口袋公园内",
            "opening_hours": "全天开放",
            "description": "面向周边居民的便民运动区域。",
            "service_content": "健身器材、休息座椅",
            "target_people": "居民、老年人",
            "image_url": "",
            "is_featured": False,
            "status": "published",
        },
        headers=headers,
    )
    assert create_response.status_code == 201

    search_response = client.get("/api/points", params={"keyword": "晨曦公益运动角"})
    assert search_response.status_code == 200
    assert search_response.json()["total"] >= 1


def test_admin_lists_load_successfully():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    points_response = client.get("/api/admin/points", headers=headers)
    assert points_response.status_code == 200
    points_payload = points_response.json()
    assert "items" in points_payload
    assert "total" in points_payload

    news_response = client.get("/api/admin/news", headers=headers)
    assert news_response.status_code == 200
    news_payload = news_response.json()
    assert "items" in news_payload
    assert "total" in news_payload
