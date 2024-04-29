from fastapi import FastAPI

from schemas import CarModel, CarModelCreate
from models import CarModelDict, CarModelClass

app = FastAPI()

@app.get("/cars", response_model=list[CarModel])
async def all_cars() -> list[CarModelDict]:
    return[
        {"id": 1, "make": "Toyota", "model": "Highlander", "year": 2024, "color": "red", "price": 1234.56},
        {"id": 2, "make": "Honda", "model": "Civic", "year": 2014, "color": "blue", "price": 9876.54},
    ]

@app.post("/cars", response_model=CarModel)
async def create_car(car: CarModelCreate) -> CarModelClass:
    print(car)

    return CarModelClass(1,car.make, car.model, car.year, car.color, car.price)

@app.post("/cars2", response_model=CarModel)
async def create_car2(car: CarModelCreate) -> CarModelDict:
    print(car)

    return {"id": 1, "make": car.make, "model": car.model, "year": car.year, "color": car.color, "price": car.price}

