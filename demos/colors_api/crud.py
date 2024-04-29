from sqlalchemy.orm import Session

import models
import schemas

def get_colors(db: Session) -> list[models.Color]:
    return db.query(models.Color).all()

def create_color(db: Session, color: schemas.ColorCreate) -> models.Color:
    db_color = models.Color(name=color.name, hex_code=color.hex_code)
    db.add(db_color)
    db.commit()
    db.refresh(db_color)
    return db_color

