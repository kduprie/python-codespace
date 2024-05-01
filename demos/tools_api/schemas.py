from pydantic import BaseModel

class BaseCar(BaseModel):
    make: str
    model: str
    year: int
    color: str
    price: float

class CarCreate(BaseCar):
    ...

class Car(BaseCar):
    id: int

    class Config:
        from_attributes = True

class BaseColor(BaseModel):
    name: str
    hex_code: str

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
