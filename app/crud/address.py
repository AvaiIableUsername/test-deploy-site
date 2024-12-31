from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import select

from models.user import Address, User
from schemas.user import UserAddress


class AddressRepository:
    async def get_address(self, address_id: int, session: AsyncSession):
        stmt = select(Address).where(Address.id == address_id)
        return session.execute(stmt).scalar()

    async def add_user_address(
        self, user_id, address: UserAddress, session: AsyncSession
    ):
        book_data = address.model_dump()

        book_to_db = Address(**book_data)

        book_to_db.user_id = user_id

        session.add(book_to_db)
        await session.commit()
        return book_data

    async def del_user_address(self, address_id: int, session: AsyncSession):
        address_to_delete = self.get_address(address_id, session)

        if address_to_delete is not None:
            await session.delete(address_to_delete)
            await session.commit()
            return {}

        return None
