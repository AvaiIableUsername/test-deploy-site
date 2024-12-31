from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Address
from models.user import User
from schemas.user import UserCreate, UserAddress

from core.password_hash import get_password_hash


class UserService:
    async def get_user_by_email(self, email, session: AsyncSession):
        stmt = select(User).where(User.email == email)
        res = await session.scalar(stmt)
        return res

    async def add_new_user(self, user: UserCreate, session: AsyncSession):
        user_data = user.model_dump()
        user_data["hash_password"] = get_password_hash(user.password1)

        del user_data["password1"]
        del user_data["password2"]

        user_db = User(**user_data)
        session.add(user_db)
        await session.commit()
        return user_db

    async def add_user_address(
        self, user_id, address: UserAddress, session: AsyncSession
    ):
        book_data = address.model_dump()

        book_to_db = Address(**book_data)

        book_to_db.user_id = user_id

        session.add(book_to_db)
        await session.commit()
        return book_data
