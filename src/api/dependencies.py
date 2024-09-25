from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description="номер страницы")]
    per_page: Annotated[int | None, Query(default=5, ge=1, lt=30, description="количество на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
