import logging

from fastapi import HTTPException, Depends
from fastapi import APIRouter
from fastapi import Form

from typing import Annotated

from datetime import datetime

from errors import AccessTokenExpired

from core.password_hash import create_jwt_token, decode_jwt_token
from dependencies import SessionDp, AccessBearerToken, RefreshBearerToken
from crud.user import UserService
from schemas.jwt import TokenInfo
from schemas.user import (
    UserCreate,
    UserCreateOutput,
    UserLogIn,
    UserAddress,
    UserId,
)
from dependencies import get_current_user


users_router = APIRouter(prefix="/users")
user_service = UserService()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@users_router.post("/create_account", response_model=UserCreateOutput)
async def create_account(data: Annotated[UserCreate, Form()], session: SessionDp):
    user = await user_service.get_user_by_email(data.email, session)
    if user:
        raise HTTPException(status_code=404)
    return await user_service.add_new_user(data, session)


@users_router.post("/login")
async def login(data: Annotated[UserLogIn, Form()], session: SessionDp) -> TokenInfo:
    res = await user_service.get_user_by_email(data.email, session)
    if not res:
        raise HTTPException(
            status_code=404, detail="Пользователя с таким email не зарегистрирован"
        )

    access_token = await create_jwt_token(data.model_dump())
    refresh_token = await create_jwt_token(data.model_dump(), refresh=True)

    return TokenInfo(access=access_token, refresh=refresh_token)


@users_router.post("/me/address", status_code=201)
async def delivery_address(
    address: Annotated[UserAddress, Form()],
    session: SessionDp,
    current_user=Depends(get_current_user),
) -> dict:
    email = current_user["user"]["email"]
    user_obj = await user_service.get_user_by_email(email, session)
    user_id = UserId.model_validate(user_obj, from_attributes=True).id
    address_data = await user_service.add_user_address(user_id, address, session)
    return address_data


@users_router.post("/refresh")
async def new_access_token(token_details=Depends(RefreshBearerToken())):
    expire_time = token_details["exp"]

    if datetime.fromtimestamp(expire_time) < datetime.now():
        raise HTTPException(status_code=403)

    access_token = await create_jwt_token(token_details["user"])
    return TokenInfo(access=access_token)


@users_router.post("/logout")
async def login_by_access_token(token_details=Depends(AccessBearerToken())):
    raise AccessTokenExpired