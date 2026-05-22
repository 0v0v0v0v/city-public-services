from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "城市公共便民点位整合平台"
    api_prefix: str = "/api"
    secret_key: str = "dev-secret-key-change-me"
    access_token_expire_minutes: int = 60 * 12
    database_url: str = "sqlite:///./app.db"
    admin_username: str = "admin"
    admin_password: str = "admin123"


settings = Settings()
