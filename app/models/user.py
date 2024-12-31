from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from core.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    hash_password: Mapped[str]
    role: Mapped[str] = mapped_column(pg.VARCHAR, nullable=False, server_default="user")
    is_verified: Mapped[bool] = mapped_column(default=False)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"id: {self.id}, email: {self.email}, role: {self.role}"


class Address(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    country: Mapped[str]
    city: Mapped[str]
    postal_code: Mapped[int]
    address_line: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"id: {self.id}, postal code: {self.postal_code}, address_line: {self.address_line}"
