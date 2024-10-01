from fastapi import APIRouter, HTTPException, Response

from sqlalchemy.exc import IntegrityError

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async  with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except IntegrityError:
            # return {"status": "500", "message": "Пользователь с таким email уже существует"}
            raise HTTPException( status_code=422, detail="Пользователь с таким email не зарегистрирован")
        await session.commit()
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    async  with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

        access_token = AuthService().create_access_token( {"user_id": user.id})

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
