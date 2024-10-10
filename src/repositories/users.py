from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserAdd, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User


    async def get_user_with_hashed_password( self, email: EmailStr):
        query = select( self.model ).filter_by( email=email )
        result = await self.session.execute( query )
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate( model )





