from src.exceptions import ObjectNotFoundException, BookingsNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_bookings( self ):
        try:
            return await self.db.bookings.get_all()
        except ObjectNotFoundException as ex:
            raise BookingsNotFoundException from ex

    async def get_my_bookings( self, user_id):
        try:
            return await self.db.bookings.get_filtered( user_id=user_id )
        except ObjectNotFoundException as ex:
            raise BookingsNotFoundException from ex

    async def add_booking(
        self,
        user_id,
        booking_data: BookingAddRequest
    ):
        room = await RoomService(self.db ).get_room_with_check( booking_data.room_id)

        room_price: int = room.price
        _booking_data = BookingAdd( user_id=user_id, price=room_price, **booking_data.model_dump())
        await self.db.bookings.add_booking( _booking_data, hotel_id=room.hotel_id)
        await self.db.commit()
