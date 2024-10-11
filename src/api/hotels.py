from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

@router.get(
    "",
    summary="получение списка всех отелей"
)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(default=None, description='Название отеля'),
    location: str | None = Query(default=None, description='Адрес отеля'),
    date_from: date = Query(example="2024-11-02"),
    date_to: date = Query(example="2024-11-07"),
):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )
    return await db.hotels.get_filtered_by_time(
        date_from = date_from,
        date_to = date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get(
    "/{hotel_id}",
    summary="получение данных по конкретному отелю"
)
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel:
        return hotel
    else:
        raise HTTPException(status_code=404, detail="Такого отеля не существует")


@router.post(
    "",
    summary="добавление отеля"
)
async def create_hotel(
    db: DBDep,
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
    ),

):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="изменение данных по отелю"
)
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep,
):
    await db.hotels.edit( hotel_data, id=hotel_id)
    await db.commit()

    return {"status": 'OK'}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно отправить name или title.</h1>"
)
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):
    await db.hotels.edit( hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": 'OK'}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля"
)
async def delete_hotel(
    hotel_id: int,
    db: DBDep,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": 'OK'}




