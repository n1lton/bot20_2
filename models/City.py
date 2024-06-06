from Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class City(Base):
    __tablename__ = 'cities'

    name: Mapped[str] = mapped_column(primary_key=True)
    storages = relationship('Storage', back_populates='city')
    region_name: Mapped[str] = mapped_column(ForeignKey('regions.name'))
    region = relationship('Region', back_populates='cities')