from datetime import date

from fastapi import Query, Body, APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import HotelNotFoundHTTPException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="получение списка всех отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Адрес отеля"),
    date_from: date = Query(examples=["2024-11-02"]),
    date_to: date = Query(examples=["2024-11-07"]),
):
    hotels = await HotelService(db).get_filtered_by_time(
        pagination=pagination,
        title=title,
        location=location,
        date_from=date_from,
        date_to=date_to,
    )

    return {"status": "OK", "data": hotels}



@router.get("/{hotel_id}", summary="получение данных по конкретному отелю")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="добавление отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель у фонтана",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="изменение данных по отелю")
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    try:
        await HotelService(db).edit_hotel(hotel_data, hotel_id = hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно отправить name или title.</h1>",
)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):
    try:
        await HotelService(db).patch_hotel(hotel_data, hotel_id, exclude_unset=True)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException

    return {"status": "OK"}
