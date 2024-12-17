from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    hash_password: Mapped[str]
    role: Mapped[str] = mapped_column(pg.VARCHAR, nullable=False, server_default='user')
