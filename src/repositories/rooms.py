from fastapi import HTTPException
from sqlalchemy import insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomAdd
from src.api.hotels import get_hotel


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

