from models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Region(Base):
    __tablename__ = 'regions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cities = relationship('City', back_populates='region', cascade='all, delete')
    message_id: Mapped[int | None]