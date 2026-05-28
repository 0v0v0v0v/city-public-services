from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

NewsStatus = Literal["draft", "published"]


class NewsBase(BaseModel):
    title: str
    summary: str
    content: str
    status: NewsStatus = "draft"


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    pass


class NewsRead(NewsBase):
    id: int
    published_at: datetime
    model_config = ConfigDict(from_attributes=True)
