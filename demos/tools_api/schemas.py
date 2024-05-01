from pydantic import BaseModel, field_validator
import re

class BaseCar(BaseModel):
    make: str
    model: str
    year: int
    color: str
    price: float

    @field_validator("year")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value < 1886:
            raise ValueError("impossible year")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value < 0.0:
            raise ValueError("price must be positive")
        return value

class CarCreate(BaseCar):
    ...

class Car(BaseCar):
    id: int

    class Config:
        from_attributes = True

class BaseColor(BaseModel):
    name: str
    hex_code: str

    @field_validator("name", "hex_code")
    @classmethod
    def validate_required(cls, value: str) -> str:
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("is required")
        return value

    @field_validator("hex_code")
    @classmethod
    def validate_hex_code(cls, value: str) -> str:
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
            raise ValueError("not a valid CSS hex code")
        return value.lower()

class ColorCreate(BaseColor):
    ...

class Color(BaseColor):
    id: int

    class Config:
        from_attributes = True

# class Color(BaseModel):
#     id: int
#     name: str
#     hex_code: str

class BaseNotification(BaseModel):
    recipient_email: str
    message: str

class NotificationCreate(BaseNotification):
    ...

class Notification(BaseNotification):
    id: int

    class Config:
        from_attributes = True


class NotifyResponse(BaseModel):
    status: str
