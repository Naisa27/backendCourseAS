from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPATCH, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async  def get_filtered_by_time(
        self,
        pagination,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        per_page = pagination.per_page or 5
        check_date_to_after_date_from( date_from=date_from,
            date_to=date_to
        )

        hotels = await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

        return hotels


    async  def get_hotel(self, hotel_id: int):
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        return hotel


    async  def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add( data )
        await self.db.commit()
        return hotel


    async  def edit_hotel(self, data: HotelAdd, hotel_id: int):
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.edit( data, id=hotel_id)
        await self.db.commit()


    async  def patch_hotel(self, data: HotelPATCH, hotel_id: int, exclude_unset: bool = False):
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.edit( data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()


    async  def delete_hotel(self, hotel_id: int):
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.delete( id=hotel_id )
        await self.db.commit()


    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one( hotel_id=hotel_id )
        except ObjectNotFoundException:
            raise HotelNotFoundException
