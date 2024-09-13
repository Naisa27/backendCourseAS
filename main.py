from fastapi import FastAPI, Query, Body
import uvicorn

from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

app = FastAPI(docs_url=None, redoc_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]

@app.get("/hotels")
def get_hotels(
    id: int | None = Query(default=None, dedescription="айдишник"),
    title: str | None = Query(default=None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name

    return {"status": 'OK'}


@app.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Можно отправить name или title.</h1>"
)
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(embed=True, default=None),
    name: str | None = Body(embed=True, default=None),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title if title else hotel['title']
            hotel['name'] = name if name else hotel['name']

    return {"status": 'OK'}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"status": 'OK'}


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": ''
    })
    return {"status": "OK"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()



if __name__== "__main__":
    uvicorn.run("main:app", reload=True)
