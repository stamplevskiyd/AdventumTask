from flask import render_template, redirect, url_for, request
import names

from backend.models import User, Event, Metric
from backend import *

from backend.utils import *


@app.route("/")
def index():
    """Main page view"""

    print("Main page!")
    return render_template('index.html')


@app.route("/users")
def users():
    """User control page"""
    return render_template('users.html', users=User.query.all())


@app.route("/create_user")
def create_user():
    """Create new user with random name"""
    name = names.get_full_name()
    try:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        print("User creating error! Check DB")
    finally:
        return redirect(url_for('users'))


@app.route("/clear_users")
def clear_users():
    """Remove all users from db"""

    User.drop()
    return redirect(url_for('users'))


@app.route("/create_event")
def create_event():
    """Create random event"""

    generate_event()
    return redirect(url_for('events'))


@app.route("/events")
def events():
    """Events list page"""

    events = Event.query.all()
    return render_template('events.html', events=events, metric_types=Metric.get_metric_types())


@app.route("/clear_events")
def clear_events():
    """Remove all events from db"""

    Event.drop()
    return redirect(url_for('events'))
