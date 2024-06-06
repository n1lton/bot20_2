from Base import Base


from sqlalchemy.orm import Mapped, mapped_column, relationship


class Region(Base):
    __tablename__ = 'regions'

    name: Mapped[str] = mapped_column(primary_key=True)
    cities = relationship('City', back_populates='region')