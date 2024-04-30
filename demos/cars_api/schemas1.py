from pydantic import BaseModel

class BaseCarModel(BaseModel):
    make: str
    model: str
    year: int
    color: str
    price: float

class CarModelCreate(BaseCarModel):
    ...

class CarModel(BaseCarModel):
    id: int

# class CarModel(BaseModel):
#     id: int
#     make: str
#     model: str
#     year: int
#     color: str
#     price: float
