from sqlalchemy import Column, Integer, String
from database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    recipient_email = Column(String)
    message = Column(String)
