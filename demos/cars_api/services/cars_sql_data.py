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
