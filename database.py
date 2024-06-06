from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Base import Base

DATABASE_NAME = 'data.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)


Base.metadata.create_all(engine)
    
db = Session(bind=engine)