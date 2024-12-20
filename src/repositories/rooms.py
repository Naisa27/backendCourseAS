from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload

from src.exceptions import WrongDateOrderException, ObjectNotFoundException, RoomsNotFoundException, RoomNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        if date_from >= date_to:
            raise WrongDateOrderException

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            # .options(joinedload(self.model.facilities))  #один запрос в БД и много данных по сети
            .options(
                selectinload(self.model.facilities)
            )  # два запроса в БД и меньше данных по сети
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        if result:
            return [
                RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.scalars().all()
            ]  # .unique() нужен при joinedload
        else:
            raise RoomsNotFoundException

    async def get_one_with_rels(self, **filter_by):
        query = select(self.model).options(joinedload(self.model.facilities)).filter_by(**filter_by)

        result = await self.session.execute(query)
        try:
            model = result.unique().scalars().one()
            return RoomDataWithRelsMapper.map_to_domain_entity(model)
        except NoResultFound:
            raise RoomNotFoundException




