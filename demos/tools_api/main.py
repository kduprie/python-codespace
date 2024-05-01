from fastapi import FastAPI
import uvicorn

import models
from database import engine
from routers import cars, colors, notifications

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(cars.router)
app.include_router(colors.router)
app.include_router(notifications.router)

def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)

if __name__ == "__main__":
    main()
