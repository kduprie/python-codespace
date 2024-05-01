from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Callable, Any

from services.cars_sql_data import CarsSqlData
from services.notifications_sql_data import NotificationsSqlData
import models
import schemas
import logging

router = APIRouter(prefix="/cars")

CarsSqlDataType = Annotated[CarsSqlData, Depends(CarsSqlData)]
NotificationsSqlDataType = Annotated[NotificationsSqlData, Depends(NotificationsSqlData)]


@router.get("/")
async def root() -> dict[str, Any]:
    return {"message": "hello"}

@router.get("", response_model=list[schemas.Car])
async def all_cars(
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
) -> list[models.Car]:
    return cars_sql_data.get_cars()

@router.get("/{car_id}", response_model=schemas.Car)
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

@router.post("/", response_model=schemas.Car)
async def create_car(
    car: schemas.CarCreate,
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
    notifications_sql_data: Annotated[
        NotificationsSqlData, Depends(NotificationsSqlData)],
) -> models.Car:
    try:
        created_car = cars_sql_data.create_car(car)

        notifications_sql_data.create_notification(
            schemas.NotificationCreate(
                recipient_email="broker@somedomain.com",
                message=f"Added car with id {created_car.id}",
        ))
        return created_car
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal errr")

@router.put("/{car_id}", response_model=schemas.Car)
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

@router.delete("/{car_id}", response_model=schemas.Car)
async def delete_car(
    car_id: int,
    cars_sql_data: Annotated[CarsSqlData, Depends(CarsSqlData)],
    notifications_sql_data: Annotated[NotificationsSqlData,
                                      Depends(NotificationsSqlData)],
) -> models.Car:

    if car_id < 1:
        raise HTTPException(status_code=400, detail="Invalid car id")

    try:
        car_model = cars_sql_data.delete_car(car_id)
        if car_model is None:
            raise HTTPException(status_code=404, detail="Car not found")

        notifications_sql_data.create_notification(
            schemas.NotificationCreate(
                recipient_email="broker@somedomain.com",
                message=f"Deleted car with id {car_model.id}",
        ))

        return car_model
    except Exception as exc:
        logging.error("database call failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal errr")

