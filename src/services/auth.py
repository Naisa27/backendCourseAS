from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import jwt

from src.config import settings
from src.exceptions import (IncorrectTokenException, TokenHasExpiredException, ObjectNotFoundException,
                            UserNotFoundException, IncorrectPasswordException)
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenHasExpiredException


    async def add_user(self, data: UserRequestAdd):
        hashed_password = AuthService().hash_password( data.password )
        new_user_data = UserAdd( email=data.email,
            hashed_password=hashed_password
        )
        await self.db.users.add( new_user_data )
        await self.db.commit()


    async def login_user(self, data: UserRequestAdd, response) :
        user = await self.get_user_with_check(email = data.email)
        access_token = self.create_access_token( { "user_id": user.id})

        if not self.verify_password( data.password, user.hashed_password):
            raise IncorrectPasswordException

        response.set_cookie( "access_token", access_token)

        return access_token

    async def get_me( self, user_id):
        try:
            user = await self.db.users.get_one( id=user_id )
        except ObjectNotFoundException:
            raise UserNotFoundException

        return user

    async def logout_user( self, response ):
        response.delete_cookie( "access_token" )


    async def get_user_with_check(self, email: str) -> User:
        try:
            return await self.db.users.get_user_with_hashed_password(email=email)
        except ObjectNotFoundException:
            raise UserNotFoundException
