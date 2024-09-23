from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select
from src.models.hotels import HotelsOrm

from src.api.dependencies import PaginationParams, PaginationDep
from src.database import async_session_maker, engine
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, dedescription="айдишник"),
    title: str | None = Query(default=None, description='Название отеля'),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        print(type(result), result)
        hotels = result.scalars().all()
        print(type(hotels), hotels)

        return hotels

    # return hotels_[pagination.per_page * (pagination.page-1):pagination.per_page*pagination.page]


@router.put("/{hotel_id}")
def put_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name

    return {"status": 'OK'}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно отправить name или title.</h1>"
)
def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title if hotel_data.title else hotel['title']
            hotel['name'] = hotel_data.name if hotel_data.name else hotel['name']

    return {"status": 'OK'}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": 'OK'}


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            '1': {
                "summary": 'Сочи',
                'value': {
                    "title": 'Отель Сочи 5 звезд у моря',
                    "location": "ул. Моря, 1",
                }
            },
            '2': {
                "summary": 'Дубай',
                'value': {
                    "title": 'Отель Дубай у фонтана',
                    "location": "ул. Шейха, 2",
                }
            },
        }
    )
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}