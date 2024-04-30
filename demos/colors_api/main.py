from fastapi import FastAPI, Depends
from typing import Annotated
import uvicorn

from services.colors_sql_data import ColorsSqlData
import models
import schemas
from database import engine

# ensures all tables are created
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/colors", response_model=list[schemas.Color])
async def all_colors(
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> list[models.Color]:
    return colors_sql_data.get_colors()

@app.post("/colors", response_model=schemas.Color)
async def create_color(
    color: schemas.ColorCreate,
    colors_sql_data: Annotated[ColorsSqlData, Depends(ColorsSqlData)],
) -> models.Color:
    return colors_sql_data.create_color(color)

def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
    
if __name__ == "__main__":
    main()
