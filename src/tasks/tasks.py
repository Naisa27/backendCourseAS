import asyncio
from time import sleep

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from PIL import Image
import os

from src.utils.db_manager import DBManager


@celery_instance.task
def test_task(n):
    sleep(n)
    print("я молодец")


# @celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    with Image.open(image_path) as img:
        # Получаем оригинальное соотношение сторон
        aspect_ratio = img.height / img.width

        for width in sizes:
            height = int(width * aspect_ratio)
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

            filename = os.path.splitext(os.path.basename(image_path))[0]
            resized_path = os.path.join(output_folder, f"{filename}_{width}px.jpg")

            resized_img.save(resized_path, format="JPEG", quality=85)
            print(f"Изображение сохранено: {resized_path}")


async def get_bookings_with_today_checkin_helper():
    print(f"Я запускаюсь")  # noqa: F541
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
