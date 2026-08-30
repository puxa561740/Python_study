from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
)
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserResponse,
    UserLogin,
)
from app.services.user import (
    authenticate_user,
    create_user,
    get_user_by_email,
)




router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)

def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    password_hash = hash_password(
        user_data.password
    )

    user = create_user(
        db=db,
        user_data=user_data,
        password_hash=password_hash,
    )

    return user

@router.post(
    "/login",
    response_model=TokenResponse,
)

def login(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        user.id
    )

    refresh_token = create_refresh_token(
        user.id
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )