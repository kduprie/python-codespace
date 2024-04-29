from pydantic import BaseModel

class Color(BaseModel):
    id: int
    name: str
    hex_code: str

