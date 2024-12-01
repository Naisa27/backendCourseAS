from pydantic import BaseModel, Field, ConfigDict

from src.schemas.facilities import Facility


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int
    facility_ids: list[int] = []


class RoomAdd(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int
    hotel_id: int


class Room(RoomAdd):
    id: int

    # приводит ответы алхимии к схемам pydentic
    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facility_ids: list[int] = []


class RoomPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    hotel_id: int | None = None
