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
