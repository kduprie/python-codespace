import requests
from typing import cast, TypedDict

from pathlib import Path
import csv

NewColor = tuple[str, str]
Color = tuple[int,str,str]
NewColorList = list[NewColor]
ColorList = list[Color]

class ColorTypedDict(TypedDict):
    id: int
    name: str
    hex_code: str

def read_html_colors_file() -> NewColorList:
    html_colors: NewColorList = []
    with Path("html_colors.csv").open("r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        next(csv_file)
        for row in csv_file:
            html_colors.append((row[0], row[1]))
    return html_colors

def bulk_append_colors(colors: NewColorList) -> None:
    new_colors = [
        {"name": color_name, "hex_code": color_hexcode}
        for color_name, color_hexcode in colors
    ]
    print(new_colors)
    requests.post("http://127.0.0.1:8000/colors/bulk", json=new_colors)

# def append_colors(colors: list[tuple[str,str]]) -> None:
def append_colors(colors: NewColorList) -> None:
    for color_name, color_hexcode in colors:
        # new_color = {"name":"purple", "hex_code": "ff00ff"}
        new_color = {"name":color_name, "hex_code": color_hexcode}
        requests.post("http://127.0.0.1:8000/colors", json=new_color)

def load_colors(file_name: str) -> None:
    requests.post("http://127.0.0.1:8000/colors/bulk", file_name=file_name)

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
    html_colors = read_html_colors_file()
    bulk_append_colors(html_colors)
    # load_colors("html_colors.csv")

# def main() -> None:
#     append_colors([("red", "ff0000"), ("green", "00ff00"), ("blue", "0000FF")])
#     colors = get_colors()
#     print_colors(colors)

# def main() -> None:
#     new_color = {"name":"purple", "hex_code": "ff00ff"}
#     resp = requests.post("http://127.0.0.1:8000/colors", json=new_color)
#     print (resp.json())

if __name__ == "__main__":
    main()
