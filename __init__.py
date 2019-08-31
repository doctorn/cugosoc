from flask import Flask, render_template, Markup, redirect
from flaskext.markdown import Markdown

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import markdown
from markdown.extensions import tables, fenced_code

import os

from . import database

with open("maps_key") as key_file:
    maps_key = key_file.readline()

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'your_secret_key'

md = Markdown(app)
md.register_extension(tables.TableExtension)
md.register_extension(fenced_code.FencedCodeExtension)

admin = Admin(app, name='CUGOSOC', template_mode='bootstrap3')
admin.add_view(ModelView(database.Event, database.session))
admin.add_view(ModelView(database.Location, database.session))

@app.route("/")
def index():
    return (render_template(
        'index.html',
        gallery_photos=[file for file in os.listdir("./static/img/gallery/")],
        events=database.get_weeks_events()
    ))

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
    return (render_template(
        'events.html',
        events=database.get_future_events(3),
        archive=database.get_past_events(3)
    ))

@app.route("/upcoming/")
def upcoming():
    return (render_template(
        'upcoming.html',
        events=database.get_future_events()
    ))

@app.route("/past/")
def past():
    return (render_template(
        'past.html',
        events=database.get_past_events()
    ))

# Legacy redirect for BGA competitions page
@app.route("/competitions/trig2019.html")
def legacy():
    return redirect("/event/1")

@app.route("/event/<index>")
def event(index):
    event = database.get_event(index)
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

