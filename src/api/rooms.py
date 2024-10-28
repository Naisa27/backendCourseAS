from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.hotels import get_hotel

router = APIRouter(prefix="/hotels", tags=["номера"])

@router.get(
    "/{hotel_id}/rooms",
    summary="получение данных о всех номерах"
)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-11-02"),
    date_to: date = Query(example="2024-11-07"),
):
    hotel = await get_hotel(hotel_id=hotel_id, db=db)
    # rooms = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    if hotel:
        rooms = await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
        if rooms:
            return rooms
        else:
            raise HTTPException(status_code=422, detail="В данном отеле нет номеров")



@router.get(
    "/{hotel_id}/rooms/{rooms_id}",
    summary="получение данных о конкретном номере"
)
async def get_rooms(
    hotel_id: int,
    rooms_id: int,
    db: DBDep,
):
    hotel = await get_hotel( hotel_id=hotel_id, db=db)
    if hotel:
        room = await db.rooms.get_room_by_id(hotel_id=hotel_id, room_id=rooms_id)
        if room:
            return room
        else:
            raise HTTPException( status_code=404,
                detail="В этом отеле нет такого номера"
            )


@router.post(
    "/{hotel_id}",
    summary="добавление номеров"
)
async def add_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            '1': {
                "summary": "двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на море",
                    "price": 100,
                    "quantity": 5,
                    "facility_ids": []
                },
            },
            '2': {
                "summary": "люкс",
                "value": {
                    "title": "люкс",
                    "description": "вид на красоту",
                    "price": 500,
                    "quantity": 3,
                    "facilities_ids": []
                },
            }
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel = await get_hotel( hotel_id=hotel_id, db=db)
    if hotel:
        room = await db.rooms.add(_room_data)
        rooms_facilities_data = [ RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in
                                  room_data.facility_ids ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
        await db.commit()
        return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="полное изменение данных по номеру"
)
async def edit_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            '1': {
                "summary": "12 - двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на красивое море",
                    "price": 100,
                    "quantity": 5,
                    "facility_ids": [2, 3]
                },
            },

        }
    )
):
    _room_data = RoomAdd( hotel_id=hotel_id, **room_data.model_dump())
    hotel = await get_hotel( hotel_id=hotel_id, db=db)
    if hotel:
        await db.rooms.edit(_room_data, id=room_id)
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facility_ids)

        await db.commit()

    return {"status": 'OK'}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере"
)
async def patch_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_data: RoomPatchRequest = Body(
        openapi_examples={
            '1': {
                "summary": "12/12 - двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на красивое море",
                    "price": 100,
                    "quantity": 5,
                    "facility_ids": [1, 4]
                },
            },

        },
    )
):
    _room_data_dict = room_data.model_dump( exclude_unset=True )
    _room_data = RoomPatch( hotel_id=hotel_id, **_room_data_dict)
    hotel = await get_hotel( hotel_id=hotel_id, db=db)
    if hotel:
        await db.rooms.edit(_room_data, exclude_unset=True, id=room_id)
        if "facility_ids" in _room_data_dict:
            await db.rooms_facilities.set_room_facilities( room_id, facilities_ids=_room_data_dict["facility_ids"])
        await db.commit()

    return {"status": 'OK'}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="удаление данных о номере"
)
async def delete_room(
    hotel_id:int,
    room_id: int,
    db: DBDep,
):
    hotel = await get_hotel( hotel_id=hotel_id, db=db)
    if hotel:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await db.commit()

    return {"status": 'OK'}
