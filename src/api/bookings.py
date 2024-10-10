from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddPeriod, BookingAdd

router = APIRouter(prefix="/bookings", tags=["бронирования"])


@router.post(
    "/{room_id}/",
    summary="добавление бронирования"
)
async def add_booking(
    room_id: int,
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddPeriod = Body(
        openapi_examples={
            '1': {
                "summary": "двухместный",
                "value": {
                    "date_from": "2024-11-01",
                    "date_to": "2024-11-10"
                },
            },
            '2': {
                "summary": "люкс",
                "value": {
                    "date_from": "2024-12-05",
                    "date_to": "2024-12-12"
                },
            }
        }
    ),
):
    result = await db.rooms.get_one_or_none(id=room_id)
    _booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        price = result.price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
