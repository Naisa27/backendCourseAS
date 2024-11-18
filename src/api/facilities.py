from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["удобства"])


@router.get(
    "",
    summary="Получение всех удобств"
)
@cache(expire=10)
async def get_facilities(db: DBDep):
    print('go to db')
    return await db.facilities.get_all()


@router.post(
    "",
    summary="Добавление удобства"
)
async def add_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body()
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay(5)

    return {"status": "ok", "data": facility}
