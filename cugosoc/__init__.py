from flask import Flask, render_template, Markup, redirect, jsonify
from flaskext.markdown import Markdown

from flask_admin import Admin
from flask_admin.contrib import sqla

from flask_sqlalchemy import SQLAlchemy

from flask_basicauth import BasicAuth

from flask_mail import Mail, Message

from flask_migrate import Migrate

import markdown
from markdown.extensions import tables, fenced_code

from werkzeug import Response
from werkzeug.exceptions import HTTPException

from datetime import date, timedelta

from secrets import token_urlsafe

import cugosoc.grading_utils

import os

app = Flask(__name__, instance_relative_config=True)
app.jinja_env.auto_reload = True
app.config.from_pyfile('config.py')

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

class LadderParticipant(db.Model):
    __tablename__ = "ladder_participants"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True)
    rank = db.Column(db.Integer, nullable=False, default=0)
    initial = db.Column(db.Integer, nullable=False, default=0)
    visible = db.Column(db.Boolean, nullable=False, default=False)
    played = db.Column(db.Integer, nullable=False, default=0)

    def format_rank(self, modifier=0):
        rank = self.rank + modifier
        if rank < 0:
            rank = 0
        if grading_utils.max_stars(rank) != 0:
            return "%s [%d/%d stars]" % (
                grading_utils.grade(rank),
                grading_utils.stars(rank),
                grading_utils.max_stars(rank)
            )
        else:
            return grading_utils.grade(rank)

class LadderResultRequest(db.Model):
    __tablename__ = "ladder_result_requests"
    winner_token = db.Column(db.String(64), primary_key=True, nullable=False)
    loser_token = db.Column(db.String(64), primary_key=True, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey(LadderParticipant.id), nullable=False)
    loser_id = db.Column(db.Integer, db.ForeignKey(LadderParticipant.id), nullable=False)
    winner_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    loser_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, winner_id, loser_id):
        self.winner_id = winner_id
        self.loser_id = loser_id
        self.winner_token = token_urlsafe(32)
        self.loser_token = token_urlsafe(32)

md = Markdown(app)
md.register_extension(tables.TableExtension)
md.register_extension(fenced_code.FencedCodeExtension)

basic_auth = BasicAuth(app)

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ModelView(sqla.ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())

admin = Admin(app, name='CUGOSOC', template_mode='bootstrap3')
admin.add_view(ModelView(Event, db.session, name="Events"))
admin.add_view(ModelView(Location, db.session, name="Locations"))
admin.add_view(ModelView(Committee, db.session))
admin.add_view(ModelView(LadderParticipant, db.session, name="Ladder"))
admin.add_view(ModelView(LadderResultRequest, db.session, name="Requests"))

@app.route("/")
def index():
    return (render_template(
        'index.html',
        gallery_photos=[file for file in os.listdir("./cugosoc/static/img/gallery/")],
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
    rule_files = os.listdir("./cugosoc/rules")
    rule_files.sort()
    for current in rule_files:
        with open('./cugosoc/rules/' + current, 'r') as rules_file:
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
    return redirect("https://cugosoc.soc.srcf.net/event/1")

@app.route("/event/<index>")
def event(index):
    event = get_event(index)
    if event is not None and event.description is not None and event.description != "":
        with open('./cugosoc/events/' + event.description, 'r') as description_file:
            desc = description_file.read()
            return (render_template(
                'event.html',
                event=event,
                desc=desc,
                maps_key=app.config["MAPS_KEY"]
            ))
    elif event is not None:
        return (render_template(
            'event.html',
            event=event, maps_key=app.config["MAPS_KEY"]
        ))
    else:
        return page_not_found(None)

@app.route("/ladder/")
def ladder():
    return render_template('ladder.html', ladder=get_ladder())

@app.route("/join/")
def membership():
    return render_template('join.html')

@app.route("/archive/")
def archive():
    tesuji = [file for file in os.listdir("./cugosoc/static/tesuji/")]
    tesuji.sort()
    return (render_template('archive.html',
        tesuji=tesuji,
        photos=[file for file in os.listdir("./cugosoc/static/img/archive/")]
    ))

@app.route("/constitution/")
def constitution():
    return render_template('constitution.html')

@app.route("/submit/<winner_id>/<loser_id>")
def submit(winner_id, loser_id):
    if winner_id == loser_id:
        return jsonify({
            "status": "error",
            "error": "Winner and loser cannot be the same person",
        })
    else:
        winner = get_player(winner_id)
        loser = get_player(loser_id)
        if winner is None or loser is None:
            return jsonify({
                "status": "error",
                "error": "An internal error occured, please try again",
            })
        else:
            request = LadderResultRequest(winner_id, loser_id)
            db.session.add(request)
            db.session.commit()
            send_ladder_emails(winner, loser, request.winner_token, request.loser_token)
            return jsonify({ "status": "ok" })
        

@app.route('/confirm/<token>')
def confirm(token):
    request = (
        LadderResultRequest.query
            .filter(
                db.or_(
                    token == LadderResultRequest.winner_token,
                    token == LadderResultRequest.loser_token,
                )
            )
            .first()
    )
    if request is not None:
        print(token)
        print(request.winner_token)
        print(request.loser_token)
        if request.winner_token == token:
            request.winner_confirmed = True
        elif request.loser_token == token:
            request.loser_confirmed = True
        
        if request.winner_confirmed and request.loser_confirmed:
            winner = get_player(request.winner_id)
            loser = get_player(request.loser_id)
            winner.played += 1
            loser.played += 1
            winner.rank += 1
            loser.rank -= 1
            if loser.rank < 0:
                loser.rank = 0

    db.session.commit()
    return redirect("https://cugosoc.soc.srcf.net/ladder/")

@app.route('/admin/logout')
def logout():
    raise AuthException("Logged out.")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def send_ladder_emails(winner, loser, winner_token, loser_token):
    subject = "[CUGOSOC] %s vs %s result confirmation" % (winner.name, loser.name)
    msg = Message(
        html=render_template(
            'confirmation.html',
            name=winner.name,
            opponent_name=loser.name,
            before=winner.format_rank(),
            after=winner.format_rank(modifier=1),
            token=winner_token,
        ),
        subject=subject,
        recipients=[winner.email]
    )
    mail.send(msg)
    msg = Message(
        html=render_template(
            'confirmation.html',
            name=loser.name,
            opponent_name=winner.name,
            before=loser.format_rank(),
            after=loser.format_rank(modifier=-1),
            token=loser_token,
        ),
        subject=subject,
        recipients=[loser.email]
    )
    mail.send(msg)

def get_player(id):
    return (
        LadderParticipant.query
            .filter(id == LadderParticipant.id)
            .first()
    )

def get_event(index):
    return (
        Event.query
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

def get_ladder():
    query = (
        LadderParticipant.query
            .order_by(db.desc(LadderParticipant.rank))
    )
    return list(
        map(lambda record: {
                "id": record.id,
                "name": record.name,
                "grade": grading_utils.grade(record.rank),
                "max_stars": grading_utils.max_stars(record.rank),
                "stars": grading_utils.stars(record.rank),
                "diff": (record.rank - record.initial),
                "visible": record.visible
            },
            query,
        )
    )
