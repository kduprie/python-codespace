from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from services.colors_sql_data import ColorsSqlData
import models
import schemas

router = APIRouter(prefix="/colors")

ColorsSqlDataType = Annotated[ColorsSqlData, Depends(ColorsSqlData)]

@router.get("/", response_model=list[schemas.Color])
async def all_colors(
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> list[models.Color]:
    return colors_sql_data.get_colors()

@router.get("/{color_id}", response_model=schemas.Color)
async def one_color(
    color_id: int,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    color_model = colors_sql_data.get_color(color_id)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model

@router.post("/", response_model=schemas.Color)
async def create_color(
    color: schemas.ColorCreate,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    return colors_sql_data.create_color(color)

@router.put("/{color_id}", response_model=schemas.Color)
async def replace_color(
    color_id: int,
    color: schemas.Color,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:

    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")
    if color_id != color.id:
        raise HTTPException(status_code=400, detail="Color id mismatch")

    color_model = colors_sql_data.update_color(color)
    if color_model is None:
         raise HTTPException(status_code=404, detail="Color not found")

    return color_model

@router.delete("/{color_id}", response_model=schemas.Color)
async def delete_color(
    color_id: int,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    color_model = colors_sql_data.delete_color(color_id)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model

