from fastapi import Query, Body, APIRouter

from repositories.hotels import HotelsRepository

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description='Название отеля'),
    location: str | None = Query(default=None, description='Адрес отеля'),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get(
    "/{hotel_id}",
    summary="Получение данных конкретного отеля"
)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return hotel if hotel else {"detail": "Такого отеля нет"}


@router.put("/{hotel_id}")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelAdd
):
    async with async_session_maker() as session:
        await HotelsRepository( session ).edit( hotel_data, id=hotel_id)
        await session.commit()

    return {"status": 'OK'}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно отправить name или title.</h1>"
)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    async with async_session_maker() as session:
        await HotelsRepository( session ).edit( hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": 'OK'}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": 'OK'}


@router.post("")
async def create_hotel(
    hotel_data: HotelAdd = Body(
        openapi_examples={
            '1': {
                "summary": 'Сочи',
                'value': {
                    "title": 'Отель 5 звезд у моря',
                    "location": "Сочи, ул. Моря, 1",
                }
            },
            '2': {
                "summary": 'Дубай',
                'value': {
                    "title": 'Отель у фонтана',
                    "location": "Дубай, ул. Шейха, 2",
                }
            },
        }
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


