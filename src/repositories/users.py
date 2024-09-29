from fastapi import HTTPException
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserAdd


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User
