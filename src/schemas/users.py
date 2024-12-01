from pydantic import BaseModel, ConfigDict, EmailStr


# для использования при получении запроса с клиента
class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


# для добавления в БД
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


# для возврата данных на клиент
class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# для получения хэшированного пароля из БД
class UserWithHashedPassword(User):
    hashed_password: str
