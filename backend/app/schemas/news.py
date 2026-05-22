from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NewsBase(BaseModel):
    title: str
    summary: str
    content: str
    status: str = "published"


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsRead(NewsBase):
    id: int
    published_at: datetime
    model_config = ConfigDict(from_attributes=True)
