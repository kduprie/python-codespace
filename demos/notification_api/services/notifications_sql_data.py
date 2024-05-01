from fastapi import Depends
from sqlalchemy.orm import Session

import models
import schemas
from services.get_db_session import get_db_session

class NotificationsSqlData:
    def __init__(self, db_session: Session = Depends(get_db_session)) -> None:
        self.__db_session = db_session

    def create_notification(self, notification: schemas.NotificationCreate,
                            ) -> models.Notification:
        notification_model = models.Notification(
            recipient_email = notification.recipient_email,
            message = notification.message,
        )
        self.__db_session.add(notification_model)
        self.__db_session.commit()
        self.__db_session.refresh(notification_model)
        return notification_model
