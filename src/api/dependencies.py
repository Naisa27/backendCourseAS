from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description="номер страницы")]
    per_page: Annotated[int | None, Query(default=5, ge=1, lt=30, description="количество на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get( 'access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не авторизованы")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token( token )
    return data.get("user_id", None)


UserIdDep = Annotated[int, Depends(get_current_user_id)]
