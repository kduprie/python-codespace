from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Annotated

from services.notifications_sql_data import NotificationsSqlData
import schemas
import logging


NotifcationsSqlDataType = Annotated[NotificationsSqlData,
                                    Depends(NotificationsSqlData)]

router = APIRouter(prefix="/notify")

@router.post("/", response_model=schemas.NotifyResponse)
async def create_notification(
    notification: schemas.NotificationCreate,
    notifications_sql_data: Annotated[NotificationsSqlData,
                                      Depends(NotificationsSqlData)],
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    try:
        # notifications_sql_data.create_notification(notification)
        background_tasks.add_task(
            notifications_sql_data.create_notification,
            notification,
        )
        return {"status" :"received"}
    except Exception as exc:
        logging.error("notify failed", exc_info=exc)
        raise HTTPException(status_code=500, detail="Internal errr")
