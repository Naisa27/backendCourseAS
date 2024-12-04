from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep
from src.exceptions import WrongDateOrderException, ObjectNotFoundException, ObjectMoreOneException, check_date_to_after_date_from, HotelNotFoundHTTPException, RoomNotFoundHTTPException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.hotels import get_hotel

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
        hotel = await db.hotels.get_exist_hotel( hotel_id=hotel_id )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    rooms = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )

    if rooms:
        return rooms
    else:
        raise HTTPException(status_code=422, detail="В данном отеле нет номеров")


@router.get("/{hotel_id}/rooms/{rooms_id}", summary="получение данных о конкретном номере")
async def get_room(
    hotel_id: int,
    rooms_id: int,
    db: DBDep,
):
    try:
        hotel = await db.hotels.get_exist_hotel( hotel_id=hotel_id )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        room = await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=rooms_id)
        return room
    except ObjectNotFoundException:
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        hotel = await db.hotels.get_exist_hotel( hotel_id=hotel_id )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facility_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        hotel = await db.hotels.get_exist_hotel( hotel_id=hotel_id )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.edit(_room_data, id=room_id, hotel_id = hotel_id)
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facility_ids
        )

        await db.commit()

        return {"status": "OK"}
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    except ObjectMoreOneException:
        raise HTTPException(status_code=400, detail=f"В этом отеле комнат с номером {room_id} более одной")



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
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    try:
        hotel = await db.hotels.get_exist_hotel( hotel_id=hotel_id )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id = hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    except ObjectMoreOneException:
        raise HTTPException(status_code=400, detail=f"В этом отеле комнат с номером {room_id} более одной")

    if "facility_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facility_ids"]
        )
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="удаление данных о номере")
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        hotel = await db.hotels.get_exist_hotel( hotel_id=hotel_id )
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    await db.commit()

    return {"status": "OK"}
