from fastapi import HTTPException
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserAdd


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def add( self, data: UserAdd ):
        user = await self.get_one_or_none(email=data.email)
        if user is not None:
            raise HTTPException( status_code=400, detail="Пользователь с таким мейлом уже существует")
        await super().add(data)
