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
