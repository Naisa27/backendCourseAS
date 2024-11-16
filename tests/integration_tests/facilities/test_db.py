from src.schemas.facilities import FacilityAdd


async def test_add_hotel(db):
    facility_data = FacilityAdd(
        title="интернет",
    )
    new_facility_data = await db.facilities.add(facility_data)
    print(f"{new_facility_data=}")
    await db.commit()