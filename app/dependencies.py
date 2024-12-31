from http.client import HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from core.database import db_helper

from fastapi.security import HTTPBearer
from fastapi.requests import Request

from core.password_hash import decode_jwt_token

SessionDp = Annotated[AsyncSession, Depends(db_helper.session_getter)]


class TokenBearer(HTTPBearer):
    async def __call__(self, request: Request):
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = await decode_jwt_token(token)

        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data):
        raise NotImplementedError("Переопределите метод в дочернем классе")


class AccessBearerToken(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=403, detail="Воспользуйтесь access токеном")


class RefreshBearerToken(TokenBearer):
    def verify_token_data(self, token_data):
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=403, detail="Воcпользуйтесь refresh токеном"
            )


async def get_current_user(session: SessionDp, user_data=Depends(AccessBearerToken())):
    return user_data
