from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import FacilitiesNotFoundException, FacilitiesNotFoundHTTPException
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiyService


router = APIRouter(prefix="/facilities", tags=["удобства"])


@router.get("", summary="Получение всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
    try:
        return await FacilitiyService(db).get_facilities()
    except FacilitiesNotFoundException:
        return FacilitiesNotFoundHTTPException


@router.post("", summary="Добавление удобства")
async def add_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilitiyService(db).add_facility(facility_data)

    return {"status": "ok", "data": facility}
