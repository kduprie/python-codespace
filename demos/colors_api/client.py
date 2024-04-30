import requests
from typing import cast, TypedDict

NewColor = tuple[str, str]
Color = tuple[int,str,str]
NewColorList = list[NewColor]
ColorList = list[Color]

class ColorTypedDict(TypedDict):
    id: int
    name: str
    hex_code: str


# def append_colors(colors: list[tuple[str,str]]) -> None:
def append_colors(colors: NewColorList) -> None:
    for color_name, color_hexcode in colors:
        # new_color = {"name":"purple", "hex_code": "ff00ff"}
        new_color = {"name":color_name, "hex_code": color_hexcode}
        requests.post("http://127.0.0.1:8000/colors", json=new_color)

# def get_colors() -> list[tuple[int,str,str]]:
def get_colors() -> ColorList:
    resp = requests.get("http://127.0.0.1:8000/colors")
    color_dicts = cast(list[ColorTypedDict],resp.json())

    return [
        (color_dict["id"],color_dict["name"], color_dict["hex_code"])
        for color_dict in color_dicts
    ]

# def print_colors(colors: list[tuple[int,str,str]]) -> None:
def print_colors(colors: ColorList) -> None:
    for id, name, hex_code in colors:
        print(f"id: {id}, name: {name}, hex_code: {hex_code}")

def main() -> None:
    append_colors([("red", "ff0000"), ("green", "00ff00"), ("blue", "0000FF")])
    colors = get_colors()
    print_colors(colors)

# def main() -> None:
#     new_color = {"name":"purple", "hex_code": "ff00ff"}
#     resp = requests.post("http://127.0.0.1:8000/colors", json=new_color)
#     print (resp.json())

if __name__ == "__main__":
    main()