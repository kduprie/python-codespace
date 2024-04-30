from pydantic import BaseModel

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

