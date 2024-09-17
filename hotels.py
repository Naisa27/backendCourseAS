from typing import Annotated

from fastapi import Query, Body, APIRouter, Depends

from dependencies import PaginationParams, PaginationDep
from schemas.hotels import Hotel, HotelPATCH

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(default=None, dedescription="айдишник"),
    title: str | None = Query(default=None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_[pagination.per_page * (pagination.page-1):pagination.per_page*pagination.page]


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
def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            '1': {
                "summary": 'Сочи',
                'value': {
                    "title": 'Отель Сочи 5 звезд у моря',
                    "name": "sochi_u_morya",
                }
            },
            '2': {
                "summary": 'Дубай',
                'value': {
                    "title": 'Отель Дубай у фонтана',
                    "name": "dubai_fountain",
                }
            },
        }
    )
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": ''
    })
    return {"status": "OK"}