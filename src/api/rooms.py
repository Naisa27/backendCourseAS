from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import check_date_to_after_date_from, HotelNotFoundHTTPException, RoomNotFoundHTTPException, RoomsNotFoundException, RoomsNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException, RoomsMoreOneException, RoomsMoreOneHTTPException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["номера"])


@router.get("/{hotel_id}/rooms", summary="получение данных о всех номерах")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2024-11-02"]),
    date_to: date = Query(examples=["2024-11-07"]),
):
    check_date_to_after_date_from(date_from=date_from, date_to=date_to)

    try:
        rooms = await RoomService(db).get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )
        return rooms
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomsNotFoundException:
        raise RoomsNotFoundHTTPException



@router.get("/{hotel_id}/rooms/{rooms_id}", summary="получение данных о конкретном номере")
async def get_room(
    hotel_id: int,
    rooms_id: int,
    db: DBDep,
):
    try:
        room = await RoomService(db).get_room( hotel_id=hotel_id, rooms_id=rooms_id )
        return room
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException





@router.post("/{hotel_id}", summary="добавление номеров")
async def add_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на море",
                    "price": 100,
                    "quantity": 5,
                    "facility_ids": [],
                },
            },
            "2": {
                "summary": "люкс",
                "value": {
                    "title": "люкс",
                    "description": "вид на красоту",
                    "price": 500,
                    "quantity": 3,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    try:
        room = await RoomService(db).add_room( hotel_id = hotel_id, room_data = room_data )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="полное изменение данных по номеру")
async def edit_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "12 - двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на красивое море",
                    "price": 100,
                    "quantity": 5,
                    "facility_ids": [2, 3],
                },
            },
        }
    ),
):
    try:
        await RoomService(db).edit_room(hotel_id = hotel_id, room_id = room_id, room_data = room_data)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomsMoreOneException:
        raise RoomsMoreOneHTTPException



@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление данных о номере")
async def patch_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_data: RoomPatchRequest = Body(
        openapi_examples={
            "1": {
                "summary": "12/12 - двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на красивое море",
                    "price": 100,
                    "quantity": 5,
                    "facility_ids": [1, 4],
                },
            },
        },
    ),
):
    try:
        await RoomService(db).patch_room(hotel_id = hotel_id, room_id = room_id, room_data = room_data)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except RoomsMoreOneException:
        raise RoomsMoreOneHTTPException


@router.delete("/{hotel_id}/rooms/{room_id}", summary="удаление данных о номере")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await RoomService(db).delete_room(hotel_id = hotel_id, room_id = room_id)

    return {"status": "OK"}
