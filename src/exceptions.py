from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = 'Объект не найден'


class AllRoomsAreBookedException(NabronirovalException):
    detail = 'Все номера забронированы'


class ItExistsException(NabronirovalException):
    detail = 'Такой объект уже существует'


class WrongDateOrderException(NabronirovalException):
    detail = 'Неверный порядок дат'


class ObjectMoreOneException(NabronirovalException):
    detail = 'Объектов более одного'


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


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(status_code=422, detail="Дата отъезда не может быть меньше даты выезда")
