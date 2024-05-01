from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
import uvicorn
import logging

from services.notifications_sql_data import NotificationsSqlData
import models
import schemas
from database import engine

models.Base.metadata.create_all(bind=engine)

NotifcationsSqlDataType = Annotated[NotificationsSqlData,
                                    Depends(NotificationsSqlData)]

app = FastAPI()

@app.post("/notify", response_model=schemas.NotifyResponse)
async def create_notification(
    notification: schemas.NotificationCreate,
    notifications_sql_data: Annotated[NotificationsSqlData,
                                      Depends(NotificationsSqlData)],
) -> dict[str, str]:
    try:
        notifications_sql_data.create_notification(notification)
        return {"status" :"received"}
    except Exception as exc:
        logging.error("notify failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal errr")

def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)

if __name__ == "__main__":
    main()
