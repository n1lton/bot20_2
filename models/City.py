from models.Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    storages = relationship('Storage', back_populates='city', cascade='all, delete')
    region_id: Mapped[str] = mapped_column(
        ForeignKey('regions.id', ondelete='CASCADE')
    )
    region = relationship('Region', back_populates='cities')