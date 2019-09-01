from flask import Flask, render_template, Markup, redirect
from flaskext.markdown import Markdown

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_sqlalchemy import SQLAlchemy

import markdown
from markdown.extensions import tables, fenced_code

from datetime import date, timedelta

import os

with open("maps_key") as key_file:
    maps_key = key_file.readline()

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.name + " (" + self.address + ")"

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.Integer, db.ForeignKey(Location.id), nullable=False)
    location_data = db.relationship('Location')
    date = db.Column(db.Date, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    tournament = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.String(64), default="")
    facebook_link = db.Column(db.String(64), default="")

class Committee(db.Model):
    __tablename__ = "committee_members"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64))
    role = db.Column(db.String(64), nullable=False)
    index = db.Column(db.Integer, nullable=False, default=0)
    active = db.Column(db.Boolean, nullable=False)

md = Markdown(app)
md.register_extension(tables.TableExtension)
md.register_extension(fenced_code.FencedCodeExtension)

admin = Admin(app, name='CUGOSOC', template_mode='bootstrap3')
admin.add_view(ModelView(Event, db.session, name="Events"))
admin.add_view(ModelView(Location, db.session, name="Locations"))
admin.add_view(ModelView(Committee, db.session))

@app.route("/")
def index():
    return (render_template(
        'index.html',
        gallery_photos=[file for file in os.listdir("./static/img/gallery/")],
        events=get_weeks_events()
    ))

@app.route("/about/")
def about():
    return render_template(
            'about.html',
            committee=(
                Committee.query
                    .filter(Committee.active)
                    .order_by(db.asc(Committee.index))
            )
    )

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
    return (render_template(
        'events.html',
        events=get_future_events(3),
        archive=get_past_events(3)
    ))

@app.route("/upcoming/")
def upcoming():
    return (render_template(
        'upcoming.html',
        events=get_future_events()
    ))

@app.route("/past/")
def past():
    return (render_template(
        'past.html',
        events=get_past_events()
    ))

# Legacy redirect for BGA competitions page
@app.route("/competitions/trig2019.html")
def legacy():
    return redirect("/event/1")

@app.route("/event/<index>")
def event(index):
    event = get_event(index)
    if event is not None and event.description is not None:
        with open('events/' + event.description, 'r') as description_file:
            desc = description_file.read()
            return (render_template(
                'event.html',
                event=event,
                desc=desc,
                maps_key=maps_key
            ))
    elif event is not None:
        return (render_template(
            'event.html',
            event=event, maps_key=maps_key
        ))
    else:
        return page_not_found(None)

@app.route("/join/")
def membership():
    return render_template('join.html')

@app.route("/archive/")
def archive():
    tesuji = [file for file in os.listdir("./static/tesuji/")]
    tesuji.sort()
    return (render_template('archive.html',
        tesuji=tesuji,
        photos=[file for file in os.listdir("./static/img/archive/")]
    ))

@app.route("/constitution/")
def constitution():
    return render_template('constitution.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def get_event(index):
    return (
        session.query(Event)
            .filter(index == Event.id)
            .first()
    )

def get_future_events(limit=0):
    query = (
        Event.query
            .order_by(db.asc(Event.date))
            .filter(date.today() <= Event.date)
    )
    if limit != 0:
        query = query.limit(limit)
    return query

def get_weeks_events(limit=0):
    query = (
        Event.query
            .order_by(db.asc(Event.date))
            .filter(date.today() + timedelta(weeks=1) > Event.date)
            .filter(date.today() <= Event.date)
    )
    if limit != 0:
        query = query.limit(limit)
    return query

def get_past_events(limit=0):
    query = (
        Event.query
            .filter(date.today() > Event.date)
            .order_by(db.desc(Event.date))
    )
    if limit != 0:
        query = query.limit(limit)
    return query
