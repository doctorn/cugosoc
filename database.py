from sqlalchemy import *
from sqlalchemy import sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from datetime import date, timedelta

Base = declarative_base()
engine = create_engine("sqlite:///data.db")

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    address = Column(String(128))

    def __repr__(self):
        return self.name + " (" + self.address + ")"

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    location_id = Column(Integer, ForeignKey(Location.id))
    location = relationship('Location')
    date = Column(Date)
    start = Column(Time)
    end = Column(Time)
    tournament = Column(Boolean, default=False)
    description = Column(String(64), default="")
    facebook_link = Column(String(64), default="")

def get_event(index):
    return (
        session.query(Event)
            .filter(index == Event.id)
            .first()
    )

def get_future_events(limit=0):
    query = (
        session.query(Event)
            .order_by(asc(Event.date))
            .filter(date.today() <= Event.date)
    )
    if limit != 0:
        query = query.limit(limit)
    return query

def get_weeks_events(limit=0):
    query = (
        session.query(Event)
            .order_by(asc(Event.date))
            .filter(date.today() + timedelta(weeks=1) > Event.date)
            .filter(date.today() <= Event.date)
    )
    if limit != 0:
        query = query.limit(limit)
    return query

def get_past_events(limit=0):
    query = (
        session.query(Event)
            .filter(date.today() > Event.date)
            .order_by(desc(Event.date))
    )
    if limit != 0:
        query = query.limit(limit)
    return query

"""
def process(rows):
    events = []
    for row in rows:
        event = dict(row.items())
        event["date"] = event["date"].strftime('%d/%m/%Y')
        event["start"] = event["start"].strftime('%H:%M')
        event["end"] = event["end"].strftime('%H:%M')
        print(event)
        events.append(event)
    return events
"""
