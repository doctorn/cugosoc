from sqlalchemy import create_engine, MetaData, sql
from sqlalchemy import Table, Column, Integer, String, Boolean, Date, Time, Binary, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///data.db")

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    address = Column(String(128))

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    location = Column(ForeignKey(Location.id))
    date = Column(Date)
    start = Column(Time)
    end = Column(Time)
    tournament = Column(Boolean, default=False)
    description = Column(String(64), default="")
    facebook_link = Column(String(64), default="")

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
