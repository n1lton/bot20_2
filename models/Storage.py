from Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Storage(Base):
    __tablename__ = 'storages'

    name: Mapped[str] = mapped_column(primary_key=True)
    city_name: Mapped[str] = mapped_column(ForeignKey('cities.name'))
    city = relationship('City', back_populates='storages')