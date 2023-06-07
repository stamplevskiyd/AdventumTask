import io
import csv
from flask import render_template, redirect, url_for,  send_file

from backend import *
from backend.utils import *


@app.route("/")
@app.route("/events")
def events():
    """Events list page"""
    return render_template(
        'events.html',
        events=models.Event.query.all(),
        metric_types=models.Metric.TYPES
    )


@app.route("/users")
def users_list():
    """User control page"""
    return render_template(
        'users.html',
        users=models.User.query.all(),
    )


@app.route("/create_user")
def create_user():
    """Create new user with random name"""
    user = models.User(name=names.get_full_name())
    db_functions.save_object(user)
    return redirect(url_for('users_list'))


@app.route("/clear_users")
def clear_users():
    """Remove all users from db"""
    db_functions.clear_table(models.User)
    return redirect(url_for('users_list'))


@app.route("/create_event")
def create_event():
    """Create random event"""
    generate_event()
    return redirect(url_for('events'))


@app.route("/clear_events")
def clear_events():
    """Remove all events from db"""
    db_functions.clear_table(models.Event)
    return redirect(url_for('events'))


@app.route("/start_modeling")
def start_modeling():
    """Erases all old data and starts new modeling"""
    init_modeling()
    return redirect(url_for('events'))


@app.route("/save_to_csv")
def save_to_csv():
    """Saves current events to csv file"""
    proxy = io.StringIO()
    writer = csv.writer(proxy)

    metric_types = models.Metric.TYPES
    header = ['event_id', 'user_id', 'datetime', 'type', 'source', 'browser_type', *metric_types]

    writer.writerow(header)
    for event in models.Event.query.order_by(models.Event.event_datetime):
        event_metrics = event.get_typed_metrics()
        row = [
            event.id, event.user.id,
            event.event_datetime.strftime("%d-%m-%Y %H:%M:%S"),
            event.get_pretty_type, event.source, event.browser_type,  # Может, стоит вернуть тип в виде числа
            *[event_metrics[metric_type] for metric_type in metric_types]
        ]
        writer.writerow(row)

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode())
    mem.seek(0)
    proxy.close()
    return send_file(
        mem,
        as_attachment=True,
        download_name='events.csv',
        mimetype='text/csv'
    )
