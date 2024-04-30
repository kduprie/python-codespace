from fastapi import Depends
from sqlalchemy.orm import Session

import models
import schemas
from services.get_db_session import get_db_session

class ColorsSqlData:
    def __init__(self, db_session: Session = Depends(get_db_session)) -> None:
        self.__db_session = db_session

    def get_colors(self) -> list[models.Color]:
        return self.__db_session.query(models.Color).all()

    def get_color(self, color_id: int) -> models.Color | None:
        return (
            self.__db_session.query(models.Color)
            .filter(models.Color.id == color_id)
            .first()
        )

    def create_color(self, color: schemas.ColorCreate) -> models.Color:
        color_model = models.Color(name=color.name, hex_code=color.hex_code)
        self.__db_session.add(color_model)
        self.__db_session.commit()
        self.__db_session.refresh(color_model)
        return color_model

    def update_color(self, color: schemas.Color) -> models.Color | None:
        color_model = self.get_color(color.id)
        if color_model is None:
            return None

        color_model.name = color.name
        color_model.hex_code = color.hex_code
        self.__db_session.commit()
        self.__db_session.refresh(color_model)
        return color_model

    def delete_color(self, color_id: int) -> models.Color | None:
        color_model = self.get_color(color_id)
        if color_model is None:
            return None

        self.__db_session.delete(color_model)
        self.__db_session.commit()
        return color_model

