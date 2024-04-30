from fastapi import Depends
from sqlalchemy.orm import Session

import models
import schemas
from services.get_db_session import get_db_session

class CarsSqlData:
    def __init__(self, db_session: Session = Depends(get_db_session)) -> None:
        self.__db_session = db_session

    def get_cars(self) -> list[models.Car]:
        return self.__db_session.query(models.Car).all()

    def get_car(self, car_id: int) -> models.Car | None:
        return (
            self.__db_session.query(models.Car)
            .filter(models.Car.id == car_id)
            .first())

    def create_car(self, car: schemas.CarCreate) -> models.Car:
        car_model = models.Car(
            make = car.make,
            model = car.model,
            year = car.year,
            color = car.color,
            price = car.price,
        )
        self.__db_session.add(car_model)
        self.__db_session.commit()
        self.__db_session.refresh(car_model)
        return car_model

    def update_car(self, car: schemas.Car) -> models.Car | None:
        car_model = self.get_car(car.id)
        if car_model is None:
            return None

        car_model.make = car.make
        car_model.model = car.model
        car_model.year = car.year
        car_model.color = car.color
        car_model.price = car.price
        self.__db_session.commit()
        self.__db_session.refresh(car_model)
        return car_model

    def delete_car(self, car_id: int) -> models.Car | None:
        car_model = self.get_car(car_id)
        if car_model is None:
            return None

        self.__db_session.delete(car_model)
        self.__db_session.commit()
        return car_model
