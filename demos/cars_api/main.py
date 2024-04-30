from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, Any
import uvicorn

from services.cars_sql_data import CarsSqlData
import models
import schemas
from database import  engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root() -> dict[str, Any]:
    return {"message": "hello"}

@app.get("/cars", response_model=list[schemas.Car])
async def all_cars(
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
) -> list[models.Car]:
    return cars_sql_data.get_cars()

@app.post("/cars", response_model=schemas.Car)
async def create_car(
    car: schemas.CarCreate,
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
) -> models.Car:
    return cars_sql_data.create_car(car)

def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
    
if __name__ == "__main__":
    main()
