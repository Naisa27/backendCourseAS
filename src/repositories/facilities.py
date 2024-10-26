from pydantic import BaseModel
from sqlalchemy import insert, select, delete

from src.database import engine
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import current_room_facilities_ids
from src.schemas.facilities import Facility, RoomFacility, RoomFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def add_bulk( self, room_id: int, facilities_data: list[RoomFacilityAdd]):
        query_current_facilities_ids = current_room_facilities_ids(room_id=room_id)

        facilitiesIsIn = (
            query_current_facilities_ids
            .filter(self.model.facility_id.in_([ f.facility_id for f in facilities_data]))
        )
        # print( facilitiesIsIn.compile( bind=engine,
        #         compile_kwargs={
        #             "literal_binds": True
        #         }
        #     )
        # )

        result = await self.session.execute(facilitiesIsIn)

        current_facilities_ids = result.scalars().all()

        facilities_data_for_add = [f for f in facilities_data if f.facility_id not in current_facilities_ids]

        if facilities_data_for_add:
            add_data_stmt = insert( self.model ).values( [item.model_dump() for item in facilities_data_for_add] )
            await self.session.execute( add_data_stmt )



    async def delete(self, room_id: int, facilities_data: list[BaseModel]):
        current_facilities_ids = current_room_facilities_ids( room_id=room_id )

        facilitiesIsNotIn = (
            current_facilities_ids
            .filter( self.model.facility_id.not_in( [f.facility_id for f in facilities_data] ) )
        )

        result = await self.session.execute( facilitiesIsNotIn )
        facilities_data_for_del = result.scalars().all()

        if facilities_data_for_del:
            del_data_stmt= (
                delete( self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(facilities_data_for_del)
                )
            )

            await self.session.execute(del_data_stmt)
