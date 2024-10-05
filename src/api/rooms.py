from fastapi import APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.api.hotels import get_hotel

router = APIRouter(prefix="/hotels", tags=["номера"])

@router.get(
    "/{hotel_id}/rooms",
    summary="получение данных о всех номерах"
)
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await get_hotel(hotel_id=hotel_id)
        if hotel:
            rooms = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
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
    rooms_id: int
):
    async with async_session_maker() as session:
        hotel = await get_hotel( hotel_id=hotel_id )
        if hotel:
            room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=rooms_id)
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
    room_data: RoomAddRequest = Body(
        openapi_examples={
            '1': {
                "summary": "двухместный",
                "value": {
                    "title": "двухместный",
                    "description": "вид на море",
                    "price": 100,
                    "quantity": 5
                },
            },
            '2': {
                "summary": "люкс",
                "value": {
                    "title": "люкс",
                    "description": "вид на красоту",
                    "price": 500,
                    "quantity": 3
                },
            }
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        hotel = await get_hotel( hotel_id=hotel_id )
        if hotel:
            room = await RoomsRepository(session).add(_room_data)
            await session.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="полное изменение данных по номеру"
)
async def edit_room(
    room_data: RoomAddRequest,
    hotel_id: int,
    room_id: int,
):
    _room_data = RoomAdd( hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        hotel = await get_hotel( hotel_id=hotel_id )
        if hotel:
            await RoomsRepository(session).edit(_room_data, id=room_id)
            await session.commit()

    return {"status": 'OK'}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере"
)
async def patch_room(
    room_data: RoomPatchRequest,
    hotel_id: int,
    room_id: int
):
    _room_data = RoomPatch( hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        hotel = await get_hotel( hotel_id=hotel_id )
        if hotel:
            await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id)
            await session.commit()

    return {"status": 'OK'}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="удаление данных о номере"
)
async def delete_room(hotel_id:int, room_id: int):
    async with async_session_maker() as session:
        hotel = await get_hotel( hotel_id=hotel_id )
        if hotel:
            await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
            await session.commit()

    return {"status": 'OK'}
