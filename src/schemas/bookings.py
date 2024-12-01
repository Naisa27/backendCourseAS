from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingAddPeriod(BaseModel):
    date_from: date
    date_to: date


class BookingAdd(BaseModel):
    user_id: int
    price: int
    room_id: int
    date_from: date
    date_to: date

    # приводит ответы алхимии к схемам pydentic
    model_config = ConfigDict(from_attributes=True)


class Booking(BookingAdd):
    id: int

    # приводит ответы алхимии к схемам pydentic
    model_config = ConfigDict(from_attributes=True)
