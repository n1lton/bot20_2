from models.Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Storage(Base):
    __tablename__ = 'storages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    password: Mapped[str]
    expires: Mapped[int]
    message_id: Mapped[int | None]
    
    city_id: Mapped[str] = mapped_column(ForeignKey('cities.id', ondelete='CASCADE'))
    city = relationship('City', back_populates='storages')