from fastapi import APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd
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
            rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
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
    room_data: RoomAdd = Body(
        openapi_examples={
            '1': {
                "summary": "Сочи. Отель 5 звезд у моря",
                "value": {
                    "hotel_id": 12,
                    "title": "двухместный",
                    "description": "вид на море",
                    "price": 100,
                    "quantity": 5
                },
            },
            '2': {
                "summary": "Дубай. Отель у фонтана",
                "value": {
                    "hotel_id": 15,
                    "title": "люкс",
                    "description": "вид на красоту",
                    "price": 500,
                    "quantity": 3
                },
            }
        }
    ),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="полное изменение данных по номеру"
)
async def edit_room(hotel_id, room_id):
    ...


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h1>Можно отправить name или title.</h1>"
)
async def patch_room(hotel_id, room_id):
    ...


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="удаление данных о номере"
)
async def delete_room(hotel_id, room_id):
    ...
