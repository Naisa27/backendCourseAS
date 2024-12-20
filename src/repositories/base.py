import logging
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from asyncpg.exceptions import UniqueViolationError

from src.exceptions import ObjectNotFoundException, AllreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
        except NoResultFound:
            raise ObjectNotFoundException

        # from_attributes определяем в Base
        # return [ self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

        # from_attributes определяем в схемах централизовано
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        # from_attributes определяем в Base
        # return self.schema.model_validate(model, from_attributes=True)

        # from_attributes определяем в схемах централизовано
        return self.mapper.map_to_domain_entity(model)


    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)


    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
        except IntegrityError as ex:
            logging.exception(f"Не удалось добавить данные в БД. Входные данные: {data}.")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise AllreadyExistsException from ex
            else:
                logging.error(f"Незнакомая ошибка. Не удалось добавить данные в БД. Входные данные: {data}. Тип ошибки:"
                          f" {type(ex.orig.__cause__)=}")
                raise ex

        # from_attributes определяем в Base
        # return self.schema.model_validate(model, from_attributes=True)

        # from_attributes определяем в схемах централизовано
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_data_stmt)



    async def delete(self, **filter_by):
        del_data_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        await self.session.execute(del_data_stmt)
