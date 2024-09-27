from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from fastapi import HTTPException

from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select( self.model )
        result = await self.session.execute( query )
        return [ self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_one_or_none(self, **filter_by):
        query = select( self.model ).filter_by(**filter_by)
        result = await self.session.execute( query )
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)


    async def add(self, data: BaseModel):
        add_data_stmt = insert( self.model ).values( **data.model_dump() ).returning(self.model)
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute( add_data_stmt )
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)


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
            raise HTTPException(status_code=404, detail="Not found")
