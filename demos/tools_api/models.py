from sqlalchemy import Column, Integer, String, Float
from database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    color = Column(String)
    price = Column(Float)

class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    hex_code = Column(String)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    recipient_email = Column(String)
    message = Column(String)
