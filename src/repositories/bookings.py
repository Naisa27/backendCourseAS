from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, delete

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_total_cost(self):
        return await self.model.total_cost

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids = (await self.session.execute(rooms_ids_to_get)).scalars().all()
        if booking_data.room_id in rooms_ids:
            new_booking = await self.add(booking_data)
            return new_booking
        else:
            raise HTTPException(status_code=500, detail="Нет номеров для бронирования")

    async def delete_all_bookings(self):
        del_data_stmt = delete(self.model)
        await self.session.execute(del_data_stmt)
