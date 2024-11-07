import json
from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["удобства"])


@router.get(
    "",
    summary="Получение всех удобств"
)
async def get_facilities(
    db: DBDep
):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"facilities_from_cache: {facilities_from_cache}")

    if not facilities_from_cache:
        print("go to db")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)

        return  facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


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
