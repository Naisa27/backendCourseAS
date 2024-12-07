from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.exceptions import IncorrectTokenException, IncorrectTokenHTTPException
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description="номер страницы")]
    per_page: Annotated[
        int | None, Query(default=5, ge=1, lt=30, description="количество на странице")
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise  IncorrectTokenHTTPException

    return data.get("user_id", None)


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
