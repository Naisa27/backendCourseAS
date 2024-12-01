import typing
from src.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm


class FacilitiesOrm(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column( primary_key=True )
    title: Mapped[str] = mapped_column( String( 100 ) )

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities", # через какую таблицу идёт связь
    )


class RoomsFacilitiesOrm( Base ):
    __tablename__ = 'rooms_facilities'

    id: Mapped[int] = mapped_column( primary_key=True )
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey( "facilities.id"))
