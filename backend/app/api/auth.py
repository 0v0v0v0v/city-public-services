from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_db
from app.core.security import create_access_token, verify_password
from app.models.admin_user import AdminUser
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/admin/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db=Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.username == payload.username).first()
    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误。",
        )
    return TokenResponse(
        access_token=create_access_token(admin.username), username=admin.username
    )
