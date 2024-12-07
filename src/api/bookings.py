from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (AllRoomsAreBookedException, BookingsNotFoundException, BookingsNotFoundHTTPException,
                            RoomNotFoundException, RoomNotFoundHTTPException, AllRoomsAreBookedHTTPException)
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["бронирования"])


@router.get("", summary="получение всех бронирований")
async def get_bookings(db: DBDep):
    try:
        return await BookingService(db).get_bookings()
    except BookingsNotFoundException:
        raise BookingsNotFoundHTTPException


@router.get("/me", summary="получение бронирований текущего пользователя")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    try:
        return await BookingService(db).get_my_bookings(user_id)
    except BookingsNotFoundException:
        raise BookingsNotFoundHTTPException


@router.post("", summary="добавление бронирования")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "двухместный",
                "value": {
                    "room_id": 1,
                    "date_from": "2024-11-01",
                    "date_to": "2024-11-10",
                },
            },
            "2": {
                "summary": "люкс",
                "value": {
                    "room_id": 12,
                    "date_from": "2024-12-05",
                    "date_to": "2024-12-12",
                },
            },
        }
    ),
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException as ex:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
