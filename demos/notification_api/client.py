import requests


def main() -> None:
    resp = requests.get("http://localhost:8000/cars")
    print(resp.json())

    # create a new car
    new_car = {
        "make": "Toyota",
        "model": "Sienna",
        "year": 2004,
        "color": "light blue",
        "price": 30000,
    }

    # assigning to the json keyword argument should serialize new_car to
    # json and set the content-type header for the request body
    resp = requests.post("http://127.0.0.1:8000/cars", json=new_car)
    print(resp.json())


if __name__ == "__main__":
    main()
