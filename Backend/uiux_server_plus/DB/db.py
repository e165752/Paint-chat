import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///chat.sqlite3', echo=True)

def session():
    return sessionmaker(bind=engine)()
#Base.metadata.create_all(engine)
