# from typing import TypedDict
from dataclasses import dataclass
from typing_extensions import TypedDict


class ColorDict(TypedDict):
    id: int
    name: str
    hex_code: str

@dataclass
class ColorDataClass:
    id: int
    name: str
    hex_code: str