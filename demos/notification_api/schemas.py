from pydantic import BaseModel

class BaseNotification(BaseModel):
    recipient_email: str
    message: str

class NotificationCreate(BaseNotification):
    ...

class Notification(BaseNotification):
    id: int

    class Config:
        from_attributes = True


class NotifyResponse(BaseModel):
    status: str
