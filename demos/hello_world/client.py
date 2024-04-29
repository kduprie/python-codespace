import requests

def main() -> None:
    resp = requests.get("http://127.0.0.1:8000")
    print(resp.json())


if __name__ == "__main__":
    main()

