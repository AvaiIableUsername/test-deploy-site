from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from core.config import settings
from core.database import db_helper
from routers.user import users_router


@asynccontextmanager
async def life_span(app: FastAPI):
    """Подключение к базе данных"""
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=life_span)

app.mount("/static", StaticFiles(directory="../static"), name="static")


templates = Jinja2Templates(directory="../templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)

from pydantic import BaseModel


templates = Jinja2Templates(directory="../templates/html")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def registration(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def registration(request: Request):
    return templates.TemplateResponse(request=request, name="check.html")


class Cat(BaseModel):
    cat: str


@app.post("/data")
async def check(cat: Cat):
    print(cat.model_dump())
    return {"answer": cat}


if "__name__" == "__main__":
    uvicorn.run(
        app="main:app",
        port=settings.app_config.port,
        host=settings.app_config.host,
    )
