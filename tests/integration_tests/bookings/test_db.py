from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    data = BookingAdd(
        user_id=user_id,
        price=100,
        room_id=room_id,
        date_from=date( year=2024,
            month=5,
            day=1
        ),
        date_to=date( year=2024,
            month=5,
            day=10
        ),
    )
    await db.bookings.add( data )

    booking_data = BookingAdd(
        user_id=user_id,
        price=100,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
    )
    await db.bookings.add(booking_data)

    new_booking_data = await db.bookings.get_one_or_none(
        user_id=user_id,
        room_id=room_id,
        price=booking_data.price,
        date_from = booking_data.date_from,
        date_to = booking_data.date_to,
    )
    assert new_booking_data

    booking_edit_data = BookingAdd(
        user_id=user_id,
        price=200,
        room_id=room_id,
        date_from=date( year=2024, month=9, day=15),
        date_to=date( year=2024, month=9, day=23),
    )

    await db.bookings.edit(booking_edit_data, id=new_booking_data.id)

    new_booking_edit_data = await db.bookings.get_one_or_none(
        user_id=booking_edit_data.user_id,
        room_id=booking_edit_data.room_id,
        price=booking_edit_data.price,
        date_from=booking_edit_data.date_from,
        date_to=booking_edit_data.date_to,
    )
    assert new_booking_edit_data

    await db.bookings.delete(id=new_booking_edit_data.id)

    booking_data_delete = await db.bookings.get_one_or_none(
        id=new_booking_edit_data.id
    )
    assert not booking_data_delete

    await db.commit()
