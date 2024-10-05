from pydantic import BaseModel, Field, ConfigDict

class RoomAdd(BaseModel):
    title: str
    description: str | None = Field(default=None)
    price: int
    quantity: int
    hotel_id: int


class Room(RoomAdd):
    id: int

    model_config = ConfigDict( from_attributes=True )


class RoomPATCH(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)
    hotel_id: int | None = Field(default=None)
