from pydantic import BaseModel


class TokenInfo(BaseModel):
    type: str = "Bearer"
    access: str
    refresh: str = None
