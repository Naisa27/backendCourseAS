from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["бронирования"])

@router.get(
    "",
    summary="получение всех бронирований"
)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get(
    "/me",
    summary="получение бронирований текущего пользователя"
)
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="добавление бронирования"
)
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            '1': {
                "summary": "двухместный",
                "value": {
                    "room_id": 1,
                    "date_from": "2024-11-01",
                    "date_to": "2024-11-10"
                },
            },
            '2': {
                "summary": "люкс",
                "value": {
                    "room_id": 12,
                    "date_from": "2024-12-05",
                    "date_to": "2024-12-12"
                },
            }
        }
    ),
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price = room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    await db.commit()
    return {"status": "OK", "data": booking}




