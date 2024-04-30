import requests

# def main() -> None:
#     resp = requests.get("http://127.0.0.1:8000/cars")
#     print(resp.json())

def main() -> None:
    new_car = { "make": "saturn", "model" : "buck", "year": 2013 , "color": "silver" , "price": 10000}

    resp = requests.post("http://127.0.0.1:8000/cars", json=new_car)
    # resp = requests.post("http://127.0.0.1:8000/cars2", json=new_car)
    print(resp.json())


if __name__ == "__main__":
    main()