from typing import TypedDict
from dataclasses import dataclass

class CarModelDict(TypedDict):
    id: int
    make: str
    model: str
    year: int
    color: str
    price: float

@dataclass
class CarModelClass:
    id: int
    make: str
    model: str
    year: int
    color: str
    price: float
