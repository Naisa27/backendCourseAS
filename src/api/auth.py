from fastapi import APIRouter, HTTPException, Response

from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
    except IntegrityError:
        # return {"status": "500", "message": "Пользователь с таким email уже существует"}
        raise HTTPException( status_code=452, detail="Пользователь с таким email уже существует")
    await db.commit()
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    # async  with async_session_maker() as session:
    user = await db.users.get_user_with_hashed_password(email=data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")

    access_token = AuthService().create_access_token( {"user_id": user.id})

    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.put("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
