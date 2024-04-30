from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Generator, Any

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root() -> dict[str, Any]:
    return {"message": "hello"}

@app.get("/cars", response_model=list[schemas.Car])
async def all_cars(db: Session = Depends(get_db)) -> list[models.Car]:
    return crud.get_cars(db)

@app.post("/cars", response_model=schemas.Car)
async def create_car(
    car: schemas.CarCreate,
    db: Session = Depends(get_db)
) -> models.Car:

    return crud.create_car(db, car)
