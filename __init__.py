import markdown
from flask import Flask, render_template, Markup, redirect
from .database import Location, Event, engine
from sqlalchemy import sql, asc, desc
from datetime import date, timedelta
from flaskext.markdown import Markdown
from markdown.extensions import tables, fenced_code
import os

key_file = open("maps_key")
maps_key = key_file.readline()
key_file.close()

app = Flask(__name__)
# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True
md = Markdown(app)
md.register_extension(tables.TableExtension)
md.register_extension(fenced_code.FencedCodeExtension)

@app.route("/")
def index():
    return render_template('index.html', gallery_photos=[file for file in os.listdir("./static/img/gallery/")], events=get_weeks_events())

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/go/")
def go():
    rules = []
    rule_files = os.listdir("./rules")
    rule_files.sort()
    for current in rule_files:
        with open('rules/' + current, 'r') as rules_file:
            rules.append(rules_file.read())
    return render_template('go.html', rules=rules)

@app.route("/events/")
def events():
    return render_template('events.html', events=get_future_events(3), archive=get_past_events(3))

@app.route("/upcoming/")
def upcoming():
    return render_template('upcoming.html', events=get_future_events())

@app.route("/past/")
def past():
    return render_template('past.html', events=get_past_events())

# Legacy redirect for BGA competitions page
@app.route("/competitions/trig2019.html")
def legacy():
    return redirect("/event/1")

@app.route("/event/<index>")
def event(index):
    event = get_event(index)
    if event is not None and event["description"] != "":
        with open('events/' + event["description"], 'r') as description_file:
            desc = description_file.read()
            return render_template('event.html', event=event, desc=desc, maps_key=maps_key)
    elif event is not None:
        return render_template('event.html', event=event, maps_key=maps_key)
    else:
        return page_not_found(None)

@app.route("/join/")
def membership():
    return render_template('join.html')

@app.route("/archive/")
def archive():
    tesuji = [file for file in os.listdir("./static/tesuji/")]
    tesuji.sort()
    return render_template('archive.html', tesuji=tesuji, photos=[file for file in os.listdir("./static/img/archive/")])

@app.route("/constitution/")
def constitution():
    return render_template('constitution.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def get_event(index):
    conn = engine.connect()
    query = sql.select([Event.id, Event.name, Event.location, Event.date, Event.start, Event.end, Event.tournament, Event.description, Event.facebook_link]).where(Event.id == index)
    res = conn.execute(query)
    row = res.fetchone()
    if row is not None:
        event = dict(row.items())
        event["date"] = event["date"].strftime('%d/%m/%Y')
        event["start"] = event["start"].strftime('%H:%M')
        event["end"] = event["end"].strftime('%H:%M')
        query = sql.select([Location.name, Location.address]).where(Location.id == event["location"])
        res2 = conn.execute(query)
        location = res2.fetchone()
        if location is not None:
            event["location"] = dict(location.items())
        else:
            event["location"] = None
        return event
    else:
        return None

def get_future_events(limit=0):
    conn = engine.connect()
    query = sql.select([Event.id, Event.name, Event.location, Event.date, Event.start, Event.end, Event.tournament, Event.facebook_link]).where(date.today() <= Event.date)
    if limit != 0:
        query = query.limit(limit)
    query = query.order_by(asc(Event.date))
    res = conn.execute(query)
    return process(res.fetchall())

def get_weeks_events(limit=0):
    conn = engine.connect()
    query = sql.select([Event.id, Event.name, Event.location, Event.date, Event.start, Event.end, Event.tournament, Event.facebook_link]).where(date.today() + timedelta(weeks=1) > Event.date).where(date.today() <= Event.date)
    if limit != 0:
        query = query.limit(limit)
    query = query.order_by(asc(Event.date))
    res = conn.execute(query)
    return process(res.fetchall())


def get_past_events(limit=0):
    conn = engine.connect()
    query = sql.select([Event.id, Event.name, Event.location, Event.date, Event.start, Event.end, Event.tournament, Event.facebook_link]).where(date.today() > Event.date)
    if limit != 0:
        query = query.limit(limit)
    query = query.order_by(desc(Event.date))
    res = conn.execute(query)
    return process(res.fetchall())
    
def process(rows):
    conn = engine.connect()
    events = []
    for row in rows:
        event = dict(row.items())
        event["date"] = event["date"].strftime('%d/%m/%Y')
        event["start"] = event["start"].strftime('%H:%M')
        event["end"] = event["end"].strftime('%H:%M')
        query = sql.select([Location.name, Location.address]).where(Location.id == event["location"])
        res2 = conn.execute(query)
        location = res2.fetchone()
        if location is not None:
            event["location"] = dict(location.items())
        else:
            event["location"] = None
        events.append(event)
    return events

