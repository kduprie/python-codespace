from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, AsyncGenerator, Any
import uvicorn

from sqlalchemy.ext.asyncio import AsyncSession

from services.colors_sql_data import ColorsSqlData
import models
import schemas
from database import sessionmanager
# from database import engine

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    if sessionmanager.engine is None:
        raise Exception("Database engine is not initialized")
    async with sessionmanager.engine.begin() as conn:
        # await conn.run_sync(models.Base.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    if sessionmanager.engine is not None:
        # close the db engine
        await sessionmanager.close()

app = FastAPI()


@app.get("/colors", response_model=list[schemas.Color])
async def all_colors(
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> list[models.Color]:
    return await colors_sql_data.get_colors()

@app.get("/colors/{color_id}", response_model=schemas.Color)
async def one_color(
    color_id: int,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    color_model = await colors_sql_data.get_color(color_id)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model

@app.put("/colors/{color_id}", response_model=schemas.Color)
async def replace_color(
    color_id: int,
    color: schemas.Color,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:

    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")
    if color_id != color.id:
        raise HTTPException(status_code=400, detail="Color id mismatch")

    color_model = await colors_sql_data.update_color(color)
    if color_model is None:
         raise HTTPException(status_code=404, detail="Color not found")

    return color_model

@app.delete("/colors/{color_id}", response_model=schemas.Color)
async def delete_color(
    color_id: int,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    if color_id < 1:
        raise HTTPException(status_code=400, detail="Invalid color id")

    color_model = await colors_sql_data.delete_color(color_id)

    if color_model is None:
        raise HTTPException(status_code=404, detail="Color not found")

    return color_model

@app.post("/colors", response_model=schemas.Color)
async def create_color(
    color: schemas.ColorCreate,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    return await colors_sql_data.create_color(color)

def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)

if __name__ == "__main__":
    main()
