from app.core.config import settings
from app.core.security import get_password_hash
from app.models.admin_user import AdminUser
from app.models.category import Category
from app.models.news import News
from app.models.point import Point


def seed_data(db) -> None:
    if not db.query(AdminUser).first():
        db.add(
            AdminUser(
                username=settings.admin_username,
                hashed_password=get_password_hash(settings.admin_password),
            )
        )

    if not db.query(Category).first():
        categories = [
            Category(
                name="城市公园",
                slug="parks",
                icon="park",
                sort_order=1,
                description="面向居民日常休闲、散步和亲子活动的免费公共绿地。",
            ),
            Category(
                name="社区服务中心",
                slug="community-centers",
                icon="community",
                sort_order=2,
                description="提供社区事务、活动组织和基础民生服务的综合场所。",
            ),
            Category(
                name="政务服务大厅",
                slug="government-service",
                icon="service",
                sort_order=3,
                description="集中办理政务事项、便民审批和咨询服务。",
            ),
            Category(
                name="公共卫生间",
                slug="public-restrooms",
                icon="restroom",
                sort_order=4,
                description="提供免费对外开放的基础卫生设施。",
            ),
        ]
        db.add_all(categories)
        db.flush()

        db.add_all(
            [
                Point(
                    name="滨江市民公园",
                    category_id=categories[0].id,
                    address="海棠路 108 号滨江绿地入口",
                    opening_hours="全天开放",
                    description="园内包含步行道、儿童活动区和无障碍休息设施，适合家庭与老年居民休闲。",
                    service_content="休闲散步、晨练、公益活动场地",
                    target_people="周边居民、亲子家庭、老年人",
                    image_url="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80",
                    is_featured=True,
                ),
                Point(
                    name="和安社区综合服务中心",
                    category_id=categories[1].id,
                    address="和平街道和安路 66 号",
                    opening_hours="周一至周五 08:30-17:30",
                    description="提供老年助餐咨询、社区文化活动报名和基层便民窗口服务。",
                    service_content="社区咨询、活动报名、便民代办",
                    target_people="社区居民、老年人、志愿者",
                    image_url="https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=1200&q=80",
                    is_featured=True,
                ),
                Point(
                    name="市民政务服务大厅",
                    category_id=categories[2].id,
                    address="政务路 1 号市民中心一层",
                    opening_hours="周一至周五 09:00-17:00",
                    description="可集中办理社保、公积金、户籍咨询等常见事项，现场设有导办服务。",
                    service_content="政务咨询、材料受理、自助打印",
                    target_people="全体市民",
                    image_url="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
                    is_featured=False,
                ),
                Point(
                    name="人民广场东侧公共卫生间",
                    category_id=categories[3].id,
                    address="人民广场东入口旁",
                    opening_hours="06:00-22:00",
                    description="靠近地铁口与广场主通道，配有无障碍厕位和母婴护理台。",
                    service_content="免费卫生设施、无障碍服务",
                    target_people="市民、游客、老年人、儿童",
                    image_url="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
                    is_featured=True,
                ),
            ]
        )

    if not db.query(News).first():
        db.add_all(
            [
                News(
                    title="本周末社区公益书屋延长开放时间",
                    summary="部分社区书屋周末延长至晚间 8 点，方便居民借阅和参与阅读活动。",
                    content="为了满足居民周末阅读需求，多个社区公益书屋将在本周末延长开放时间，并增加亲子阅读活动场次。",
                ),
                News(
                    title="便民服务点新增无障碍设施巡检安排",
                    summary="多个便民点位启动无障碍设施检查与维护，提升特殊群体使用便利性。",
                    content="市级公共服务部门已安排本月无障碍设施巡检计划，涵盖公园、政务大厅和公共卫生间等场所。",
                ),
                News(
                    title="夏季高温期间公共避暑场所名单公布",
                    summary="社区中心、图书空间和部分体育馆将作为临时避暑开放点位。",
                    content="为应对高温天气，多个社区中心与公共阅读空间将在白天对外开放，为居民提供休息和饮水服务。",
                ),
            ]
        )

    db.commit()
