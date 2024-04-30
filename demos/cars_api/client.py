import requests
from typing import cast, TypedDict

NewCar = tuple[str, str, int, str, float]
Car = tuple[int,str,str,int,str,float]
NewCarList = list[NewCar]
CarList = list[Car]

class CarTypedDict(TypedDict):
    id: int
    make: str
    model: str
    year: int
    color: str
    price: float

def append_cars(cars: NewCarList) -> None:
    for make, model, year, color, price in cars:
        new_car = {
            "make": make,
            "model": model,
            "year": year,
            "color": color,
            "price": price,
        }
        requests.post("http://127.0.0.1:8000/cars", json=new_car)

def get_cars() -> CarList:
    resp = requests.get("http://127.0.0.1:8000/cars")
    car_dicts = cast(list[CarTypedDict], resp.json())

    return [(
        car_dict["id"],
        car_dict["make"],
        car_dict["model"],
        car_dict["year"],
        car_dict["color"],
        car_dict["price"])
        for car_dict in car_dicts
    ]

def print_cars(cars: CarList) -> None:
    for id, make, model, year, color, price in cars:
        print(f"id: {id}, make: {make}, model: {model}, year: {year}, color: {color}, price: {price}")

def main() -> None:
    append_cars([("saturnX", "blah", 2019, "red", 1),
                 ("saturnY", "foo", 2029, "pink", 100000)])
    cars = get_cars()
    print_cars(cars)

if __name__ == "__main__":
    main()
