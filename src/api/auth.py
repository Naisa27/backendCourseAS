from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (AllreadyExistsException, UserAllreadyExistsHTTPException, UserNotFoundException,
                            UserNotFoundHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException)
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        await AuthService(db).add_user(data)
    except AllreadyExistsException:
        raise UserAllreadyExistsHTTPException
    return {"status": "ok"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data, response)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    try:
        user = await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return user


@router.put("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "ok"}
