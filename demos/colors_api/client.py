import requests

def main() -> None:
    new_color = {"name":"purple", "hex_code": "ff00ff"}
    resp = requests.post("http://127.0.0.1:8000/colors", json=new_color)
    print (resp.json())

if __name__ == "__main__":
    main()