from fastapi import FastAPI

from typing import Any
from pydantic import BaseModel

from schemas import Color, ColorCreate
from models import ColorDict, ColorDataClass

app = FastAPI()


class Planet(BaseModel):
    name: str
    nearest_star: str

@app.get("/")
async def root() -> dict[str, Any]:
    return {"message": "hello"}

@app.post("/colors", response_model=Color)
async def create_color(color :ColorCreate) -> ColorDataClass:
    print(color)

    return ColorDataClass(1, color.name, color.hex_code)


# @app.get("/colors")
# async def all_colors() -> list[str]:
#     return ["red", "green", "blue"]

@app.get("/colors", response_model=list[Color])
async def all_colors() -> list[ColorDict]:
    return [
        { "id": 1, "name": "red", "hex_code": "ff0000"},
        { "id": 2, "name": "green", "hex_code": "00ff00"},
        { "id": 3, "name": "blue", "hex_code": "0000ff"},

    ]

@app.get("/colors2", response_model=list[Color])
async def all_colors2() -> list[ColorDataClass]:
    return [
        ColorDataClass(1, "red", "ff0000"),
        ColorDataClass(2, "green", "00ff00"),
        ColorDataClass(3, "blue", "0000ff"),

    ]


@app.get("/stars")
async def all_stars() -> list[str]:
    return ["polaris", "vega"]

@app.get("/planets")
async def all_planets() -> list[dict[str, Any]]:
    p1 = {"name": "Earth", "nearest_star": "Sol"}
    p2 = {"name": "Mars", "nearest_star": "Sol"}
    p3 = {"name": "Jupiter", "nearest_star": "Sol"}

    ret_list = []
    ret_list.append(p1)
    ret_list.append(p2)
    ret_list.append({"name": "Saturn", "nearest_star": "yo!"})

    # return [p1,p2,p3]
    # return[
    #     {"name": "Earth", "nearest_star": "Sol"},
    #     {"name": "Mars", "nearest_star": "Sol"},
    #     {"name": "Jupiter", "nearest_star": "still Sol"}
    # ]
    return ret_list

@app.get("/planets2")
async def some_panets() -> list[Planet]:
    p1 = Planet(name="pluto", nearest_star="a")
    p2 = Planet(name="venus", nearest_star="b")

    return [p1,p2]
