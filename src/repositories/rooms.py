from sqlalchemy import insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    # async def add(self, data: RoomAdd):
    #     add_data_stmt = insert( self.model ).values( **data.model_dump()).returning( self.model )
    #     result = await self.session.execute( add_data_stmt )
    #     model = result.scalars().one()
    #     return self.schema.model_validate( model )