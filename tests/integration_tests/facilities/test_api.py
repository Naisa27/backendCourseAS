# async def test_add_facilities(ac):
#     response = await ac.post(
#         "/facilities",
#         headers={
#             "Content-Type": "application/json"
#         },
#         json={
#             "title": "wi-fi"
#         }
#     )
#     print(f"{response.json()=}")
#
#     assert response.status_code == 200

from src.schemas.facilities import FacilityAdd


async def test_add_hotel(db):
    facility_data = FacilityAdd(
        title="интернет",
    )
    new_facility_data = await db.facilities.add(facility_data)
    print(f"{new_facility_data=}")
    await db.commit()


async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
    )
    print(f"{response.json()=}")

    assert response.status_code == 200