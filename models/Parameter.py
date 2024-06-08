from models.Base import Base
from typing import Union
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Parameter(Base):
    __tablename__ = 'parameters'

    name: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[int]