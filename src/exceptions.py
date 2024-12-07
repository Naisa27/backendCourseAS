from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = 'Объект не найден'


class IncorrectTokenException(NabronirovalException):
    detail = 'Некорректный токен'

class IncorrectPasswordException(NabronirovalException):
    detail = 'Неверный пароль'


class TokenHasExpiredException(NabronirovalException):
    detail = 'Срок действия токена истек'


class AllRoomsAreBookedException(NabronirovalException):
    detail = 'Все номера забронированы'


class RoomsNotFoundException(ObjectNotFoundException):
    detail = 'Номера отсутствуют'

class BookingsNotFoundException(ObjectNotFoundException):
    detail = 'Бронирования отсутствуют'

class FacilitiesNotFoundException(ObjectNotFoundException):
    detail = 'Удобства отсутствуют'


class RoomNotFoundException(ObjectNotFoundException):
    detail = 'Номер не найден'


class HotelNotFoundException(ObjectNotFoundException):
    detail = 'Отель не найден'


class UserNotFoundException(ObjectNotFoundException):
    detail = 'Пользователь не найден'


class AllreadyExistsException(NabronirovalException):
    detail = 'Такой объект уже существует'


class WrongDateOrderException(NabronirovalException):
    detail = 'Неверный порядок дат'


class ObjectMoreOneException(NabronirovalException):
    detail = 'Объектов более одного'


class RoomsMoreOneException(ObjectMoreOneException):
    detail = 'Номеров более одного'


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code = self.status_code, detail = self.detail)



class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Отель не найден'


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Номер не найден'


class RoomsNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'В данном отеле нет номеров'


class RoomsMoreOneHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = 'В данном отеле этих номеров более одного'


class IncorrectTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = 'Некорректный токен'


class TokenHasExpiredHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = 'Срок действия токена истек'


class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = 'Неверный пароль'


class UserAllreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = 'Такой пользователь уже существует'

class UserNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Пользователь не найден'

class BookingsNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Ни одно бронирование не найдено'


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = 'Все номера забронированы'


class FacilitiesNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = 'Удобства отсутствуют'

class NoAccessTokenHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = 'Вы не авторизованы'


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата отъезда не может быть меньше даты выезда")





