from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select( self.model )
            #.options(joinedload(self.model.facilities))  #один запрос в БД и много данных по сети
            .options(selectinload(self.model.facilities)) #два запроса в БД и меньше данных по сети
            .filter( RoomsOrm.id.in_(rooms_ids_to_get) )
        )
        result = await self.session.execute( query )
        return [RoomWithRels.model_validate( model ) for model in result.scalars().all()] # .unique() нужен при joinedload


    async def get_one_or_none_with_rels(
        self,
        **filter_by
    ):
        query = (
            select( self.model )
            .options( joinedload( self.model.facilities ) )
            .filter_by( **filter_by)
        )

        result = await self.session.execute( query )
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None

        return RoomWithRels.model_validate( model )

