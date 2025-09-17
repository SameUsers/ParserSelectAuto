from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_USER = 'postgres'
DB_PASSWORD = 'default'
DB_HOST = 'postgres'
DB_PORT = 5432
DB_NAME = 'cardb'

DB_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DB_URL, echo=False)#Создание движка

Session = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()




