import uvicorn
from fastapi import FastAPI
from errors import register_all_errors
from contextlib import asynccontextmanager


from core.config import settings
from core.database import db_helper
from routers.user import users_router


@asynccontextmanager
async def life_span(app: FastAPI):
    """Подключение к базе данных"""
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=life_span)

register_all_errors(app)


app.include_router(users_router, tags = ['User'])


if "__name__" == "__main__":
    uvicorn.run(
        app="main:app",
        port=settings.app_config.port,
        host=settings.app_config.host,
    )
