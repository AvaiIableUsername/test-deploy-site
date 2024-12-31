import logging

from datetime import timedelta, datetime
from passlib.context import CryptContext

import jwt


SECRET = "Привет :3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=1)


logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


async def create_jwt_token(
    user_data: dict, exp_time: timedelta | None = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        exp_time if exp_time is not None else ACCESS_TOKEN_EXPIRE
    )
    payload["refresh"] = refresh

    return jwt.encode(payload, key=SECRET, algorithm=ALGORITHM)


async def decode_jwt_token(user_data):
    logger.info(f"Access token: {user_data}")
    try:
        token_data = jwt.decode(user_data, key=SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError as e:
        print(e)
        return None
    return token_data
