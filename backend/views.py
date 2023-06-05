from backend.models import User, Event, Metric
from backend import *


@app.route("/")
def index():
    """Main page view"""
    print(1)
    return render_template('index.html')


@app.route("/users")
def users():
    """User control page"""
    return render_template('users.html', users=get_users())


def get_users():
    """Returns users saved in db"""
    return User.query.all()


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
        return redirect(url_for('index'))


@app.route("/clear_users")
def clear_users():
    """Remove all users from db"""
    try:
        db.session.query(User).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        return redirect(url_for('index'))


@app.route("/create_event")
def create_event():
    """Create random event"""

    # TODO: много чего недоделано

    event_types = Event.get_event_types()

    event = Event(
        type=random.choice(event_types),
        user=random.choice(get_users())
    )

    match event.type:
        case Event.SITE_VISIT:
            pass
        case Event.PHONE_CALL:
            pass
        case Event.PURCHASE:
            pass
        case Event.PURCHASE_CANCELLING:
            pass

    db.session.add(event)
    db.session.commit()

    return redirect(url_for('index'))
