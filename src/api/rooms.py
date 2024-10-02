from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd

router = APIRouter(prefix="/hotels", tags=["номера"])

@router.get("/{hotel_id}")
async def get_rooms(hotel_id):
    ...


@router.post("/{hotel_id}")
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


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id, room_id):
    ...


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление данных о номере",
    description="<h1>Можно отправить name или title.</h1>"
)
async def patch_room(hotel_id, room_id):
    ...


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id, room_id):
    ...
