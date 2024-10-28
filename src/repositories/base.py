from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from fastapi import HTTPException
from sqlalchemy.orm import joinedload


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select( self.model )
            .filter(*filter)
            .filter_by( **filter_by )
        )
        result = await self.session.execute( query )
        # from_attributes определяем в Base
        # return [ self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

        # from_attributes определяем в схемах централизовано
        return [ self.schema.model_validate(model) for model in result.scalars().all()]


    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()


    async def get_one_or_none(self, **filter_by):
        query = (
            select( self.model )
            .filter_by(**filter_by)
        )

        result = await self.session.execute( query )
        model = result.scalars().one_or_none()
        if model is None:
            return None
        # from_attributes определяем в Base
        # return self.schema.model_validate(model, from_attributes=True)

        # from_attributes определяем в схемах централизовано
        return self.schema.model_validate(model)


    async def add(self, data: BaseModel):
        add_data_stmt = insert( self.model ).values( **data.model_dump() ).returning(self.model)
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute( add_data_stmt )
        model = result.scalars().one()

        # from_attributes определяем в Base
        # return self.schema.model_validate(model, from_attributes=True)

        # from_attributes определяем в схемах централизовано
        return self.schema.model_validate(model)


    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert( self.model ).values( [ item.model_dump() for item in data] )
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute( add_data_stmt )



    async def edit(self, data: BaseModel, exclude_unset: bool=False, **filter_by):
        if await self.get_one_or_none( **filter_by ) is not None:
            edit_data_stmt = (
                update( self.model )
                .filter_by( **filter_by )
                .values( **data.model_dump(exclude_unset=exclude_unset) )
            )
            await self.session.execute( edit_data_stmt )
        elif await self.get_one_or_none( **filter_by ) is None:
            raise HTTPException(status_code=404, detail="Не найден")
        else:
            raise HTTPException(status_code=400, detail="Более одного")


    async def delete(self, **filter_by):
        del_data_stmt= delete( self.model ).filter_by(**filter_by).returning(self.model)
        if await self.get_one_or_none( **filter_by ) is not None:
            await self.session.execute( del_data_stmt )
        else:
            raise HTTPException(status_code=404, detail="Не найден")
