from sqlalchemy.orm import Session

import models
import schemas

def get_cars(db: Session) -> list[models.Car]:
    return db.query(models.Car).all()

def create_car(db: Session, car: schemas.CarCreate) -> models.Car:
    db_car = models.Car(
        make = car.make,
        model = car.model,
        year = car.year,
        color = car.color,
        price = car.price,
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car
