import atexit
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.db.base import Base
from app.main import app
from app.models.point import Point
from app.seed.data import DEFAULT_POINTS, seed_data


TEMP_DIR = tempfile.TemporaryDirectory()
TEST_DB_PATH = Path(TEMP_DIR.name) / "test_app.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
db = TestingSessionLocal()
try:
    seed_data(db)
finally:
    db.close()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def cleanup_test_db():
    engine.dispose()
    shutil.rmtree(TEMP_DIR.name, ignore_errors=True)


atexit.register(cleanup_test_db)


def get_token():
    response = client.post(
        "/api/admin/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def get_headers():
    token = get_token()
    return {"Authorization": f"Bearer {token}"}


def test_seeded_government_service_centers_are_publicly_available():
    response = client.get("/api/points", params={"keyword": "金牛政务中心", "page_size": 20})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 2
    assert {item["district"] for item in payload["items"]} == {"金牛区"}

    city_response = client.get("/api/points", params={"keyword": "政务服务中心", "page_size": 20})
    assert city_response.status_code == 200
    names = {item["name"] for item in city_response.json()["items"]}
    assert "成都市人民政府政务服务中心" in names
    assert "成华区人民政府政务服务中心" in names


def test_seeded_park_locations_are_publicly_available():
    response = client.get("/api/points", params={"keyword": "摄影公园", "page_size": 20})
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] >= 1
    assert any(item["name"] == "府河摄影公园" for item in payload["items"])

    park_response = client.get("/api/points", params={"keyword": "凤凰山公园", "page_size": 20})
    assert park_response.status_code == 200
    park_items = park_response.json()["items"]
    assert any(item["district"] == "金牛区" for item in park_items)


def test_seeded_community_service_locations_are_publicly_available():
    response = client.get("/api/points", params={"keyword": "社区卫生服务中心", "page_size": 50})
    assert response.status_code == 200
    payload = response.json()
    names = {item["name"] for item in payload["items"]}
    assert "营门口社区卫生服务中心" in names
    assert "荷花池社区卫生服务中心" in names

    service_response = client.get("/api/points", params={"keyword": "西华街道综合便民服务中心", "page_size": 20})
    assert service_response.status_code == 200
    assert any(item["name"] == "西华街道综合便民服务中心" for item in service_response.json()["items"])

    elder_response = client.get("/api/points", params={"keyword": "友联社区养老服务中心", "page_size": 20})
    assert elder_response.status_code == 200
    assert any(item["name"] == "沙河源街道友联社区养老服务中心" for item in elder_response.json()["items"])


def test_seeded_public_restrooms_are_drafts_visible_only_in_admin():
    headers = get_headers()

    admin_response = client.get(
        "/api/admin/points",
        params={"keyword": "九里堤北路1号附2号公共卫生间", "status": "draft", "page_size": 20},
        headers=headers,
    )
    assert admin_response.status_code == 200
    admin_items = admin_response.json()["items"]
    assert any(item["name"] == "九里堤北路1号附2号公共卫生间" for item in admin_items)

    public_response = client.get("/api/points", params={"keyword": "九里堤北路1号附2号公共卫生间"})
    assert public_response.status_code == 200
    assert public_response.json()["total"] == 0


def test_seed_data_does_not_duplicate_default_points():
    temp_dir = tempfile.TemporaryDirectory()
    test_db_path = Path(temp_dir.name) / "seed_idempotent.db"
    test_engine = create_engine(
        f"sqlite:///{test_db_path}",
        connect_args={"check_same_thread": False},
    )
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = testing_session()
    try:
        seed_data(db)
        first_count = db.query(Point).count()
        seed_data(db)
        second_count = db.query(Point).count()
    finally:
        db.close()
        test_engine.dispose()
        temp_dir.cleanup()

    assert first_count == len(DEFAULT_POINTS)
    assert second_count == len(DEFAULT_POINTS)


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


def test_admin_requires_auth():
    response = client.get("/api/admin/points")
    assert response.status_code == 403


def test_admin_create_and_update_category():
    headers = get_headers()
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

    list_response = client.get(
        "/api/admin/categories",
        params={"keyword": unique_suffix, "page": 1, "page_size": 10},
        headers=headers,
    )
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["total"] >= 1
    assert any(item["slug"] == f"shelters-{unique_suffix}" for item in payload["items"])


def test_admin_category_update_conflict_and_delete_guard():
    headers = get_headers()
    unique_suffix = uuid4().hex[:8]

    category_response = client.post(
        "/api/admin/categories",
        json={
            "name": f"冲突分类-{unique_suffix}",
            "slug": f"conflict-{unique_suffix}",
            "icon": "",
            "cover_image": "",
            "sort_order": 11,
            "description": "测试分类",
        },
        headers=headers,
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    conflict_response = client.put(
        f"/api/admin/categories/{category_id}",
        json={
            "name": "城市公园",
            "slug": f"conflict-{unique_suffix}",
            "icon": "",
            "cover_image": "",
            "sort_order": 11,
            "description": "测试分类",
        },
        headers=headers,
    )
    assert conflict_response.status_code == 400

    occupied_response = client.post(
        "/api/admin/categories",
        json={
            "name": f"占用分类-{unique_suffix}",
            "slug": f"occupied-{unique_suffix}",
            "icon": "",
            "cover_image": "",
            "sort_order": 12,
            "description": "带点位的分类",
        },
        headers=headers,
    )
    assert occupied_response.status_code == 201
    occupied_category_id = occupied_response.json()["id"]

    point_response = client.post(
        "/api/admin/points",
        json={
            "name": f"删除保护点位-{unique_suffix}",
            "category_id": occupied_category_id,
            "address": "测试地址 1 号",
            "opening_hours": "全天",
            "description": "用于删除保护测试。",
            "service_content": "测试服务",
            "target_people": "测试用户",
            "image_url": "",
            "is_featured": False,
            "status": "draft",
        },
        headers=headers,
    )
    assert point_response.status_code == 201

    delete_guard_response = client.delete(
        f"/api/admin/categories/{occupied_category_id}",
        headers=headers,
    )
    assert delete_guard_response.status_code == 409

    delete_point_response = client.delete(
        f"/api/admin/points/{point_response.json()['id']}",
        headers=headers,
    )
    assert delete_point_response.status_code == 200

    delete_category_response = client.delete(
        f"/api/admin/categories/{occupied_category_id}",
        headers=headers,
    )
    assert delete_category_response.status_code == 200


def test_admin_create_point_visible_in_public_search():
    headers = get_headers()
    categories = client.get("/api/admin/categories/options", headers=headers).json()
    category_id = categories[0]["id"]
    unique_suffix = uuid4().hex[:8]
    create_response = client.post(
        "/api/admin/points",
        json={
            "name": f"晨曦公益运动角-{unique_suffix}",
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

    search_response = client.get("/api/points", params={"keyword": unique_suffix})
    assert search_response.status_code == 200
    assert search_response.json()["total"] >= 1


def test_admin_point_filters_and_draft_visibility():
    headers = get_headers()
    categories = client.get("/api/admin/categories/options", headers=headers).json()
    category_id = categories[0]["id"]
    unique_suffix = uuid4().hex[:8]

    point_response = client.post(
        "/api/admin/points",
        json={
            "name": f"草稿点位-{unique_suffix}",
            "category_id": category_id,
            "address": "草稿路 18 号",
            "opening_hours": "工作日",
            "description": "草稿点位说明。",
            "service_content": "测试服务",
            "target_people": "测试居民",
            "image_url": "",
            "is_featured": True,
            "status": "draft",
        },
        headers=headers,
    )
    assert point_response.status_code == 201
    point_id = point_response.json()["id"]

    admin_point_list = client.get(
        "/api/admin/points",
        params={"keyword": unique_suffix, "category_id": category_id, "status": "draft"},
        headers=headers,
    )
    assert admin_point_list.status_code == 200
    assert admin_point_list.json()["total"] >= 1

    public_point_list = client.get("/api/points", params={"keyword": unique_suffix})
    assert public_point_list.status_code == 200
    assert public_point_list.json()["total"] == 0

    publish_point_response = client.put(
        f"/api/admin/points/{point_id}",
        json={
            "name": f"草稿点位-{unique_suffix}",
            "category_id": category_id,
            "address": "草稿路 18 号",
            "opening_hours": "工作日",
            "description": "草稿点位说明。",
            "service_content": "测试服务",
            "target_people": "测试居民",
            "image_url": "",
            "is_featured": True,
            "status": "published",
        },
        headers=headers,
    )
    assert publish_point_response.status_code == 200

    public_point_list = client.get("/api/points", params={"keyword": unique_suffix})
    assert public_point_list.status_code == 200
    assert public_point_list.json()["total"] >= 1


def test_admin_lists_load_successfully():
    headers = get_headers()

    categories_response = client.get("/api/admin/categories", headers=headers)
    assert categories_response.status_code == 200
    categories_payload = categories_response.json()
    assert "items" in categories_payload
    assert "total" in categories_payload

    points_response = client.get("/api/admin/points", headers=headers)
    assert points_response.status_code == 200
    points_payload = points_response.json()
    assert "items" in points_payload
    assert "total" in points_payload


def test_point_address_fields_round_trip():
    headers = get_headers()
    categories = client.get("/api/admin/categories/options", headers=headers).json()
    category_id = categories[0]["id"]
    unique_suffix = uuid4().hex[:8]

    create_response = client.post(
        "/api/admin/points",
        json={
            "name": f"Address Test {unique_suffix}",
            "category_id": category_id,
            "district": "Haidian",
            "street": "Zhongguancun Street",
            "address": "No. 1 Service Road",
            "landmark": "Next to Library",
            "navigation_notes": "Enter from the east gate and walk straight for 100 meters.",
            "opening_hours": "09:00-18:00",
            "description": "Address field round trip test",
            "service_content": "Testing service content",
            "target_people": "Residents",
            "image_url": "",
            "is_featured": False,
            "status": "published",
        },
        headers=headers,
    )
    assert create_response.status_code == 201
    payload = create_response.json()
    assert payload["district"] == "Haidian"
    assert payload["street"] == "Zhongguancun Street"
    assert payload["landmark"] == "Next to Library"
    assert payload["navigation_notes"] == "Enter from the east gate and walk straight for 100 meters."

    public_response = client.get("/api/points", params={"keyword": unique_suffix})
    assert public_response.status_code == 200
    assert public_response.json()["items"][0]["district"] == "Haidian"
