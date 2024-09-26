from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select( self.model )
        result = await self.session.execute( query )
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select( self.model ).filter_by(**filter_by)
        result = await self.session.execute( query )
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stmt = insert( self.model ).values( **data.model_dump() ).returning(self.model)
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute( add_data_stmt )
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by):
        edit_data_stmt = update( self.model ).filter_by( **filter_by ).values( **data.model_dump() )
        await self.session.execute( edit_data_stmt )

    async def delete(self, **filter_by):
        del_data_stmt= delete( self.model ).filter_by(**filter_by)
        await self.session.execute( del_data_stmt )
