from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["удобства"])


@router.get(
    "",
    summary="Получение всех удобств"
)
async def get_facilities(
    db: DBDep
):
    return await db.facilities.get_all()

@router.post(
    "/",
    summary="Добавление удобства"
)
async def add_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body()
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "ok", "data": facility}