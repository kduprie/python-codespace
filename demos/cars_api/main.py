import logging
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

@app.get("/cars/{car_id}", response_model=schemas.Car)
async def one_car(
    car_id: int,
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
) -> models.Car:

    if car_id < 1:
        raise HTTPException(status_code=400, detail="Invalid car id")

    try:
        car_model = cars_sql_data.get_car(car_id)
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal error")

    if car_model is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car_model

@app.put("/cars/{car_id}", response_model=schemas.Car)
async def replace_car(
    car_id: int,
    car: schemas.Car,
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
) -> models.Car:

    if car_id < 1:
        raise HTTPException(status_code=400, detail="Invalid car id")

    if car_id != car.id:
        raise HTTPException(status_code=400, detail="Car id mismatch")

    car_model = cars_sql_data.update_car(car)
    if car_model is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car_model

@app.delete("/cars/{car_id}", response_model=schemas.Car)
async def delete_car(
    car_id: int,
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
) -> models.Car:

    if car_id < 1:
        raise HTTPException(status_code=400, detail="Invalid car id")

    car_model = cars_sql_data.delete_car(car_id)
    if car_model is None:
        raise HTTPException(status_code=404, detail="Car not found")

    return car_model

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
