import csv
import datetime
import random
import names
from io import BytesIO

from backend.models import Event, User, Metric
from backend import db, config

current_time = datetime.datetime.now()


def generate_time():
    """Generates sequential random time"""
    global current_time
    current_time += datetime.timedelta(seconds=random.randint(1, 1000))
    return current_time


def generate_user():
    """Creates random user and saves in db"""
    name = names.get_full_name()
    try:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        print("User creating error! Check DB")


def generate_metric(metric_type: str) -> Metric | None:
    """Generates metric of given type"""
    metric = Metric(type=metric_type)
    match metric_type:
        case Metric.PURCHASE_PRICE:
            metric.value = random.randint(config.purchase_price_min, config.purchase_price_max)
        case Metric.PAGES_SCROLLED:
            metric.value = random.randint(config.pages_scrolled_min, config.pages_scrolled_max)
        case Metric.CALL_SUCCESS:
            metric.value = random.randint(config.call_success_min, config.call_success_max)
        case default:
            return

    return metric


def generate_event() -> None:
    """Chose random user and generate event, available for him"""
    user = random.choice(User.query.all())
    user_events = Event.query.filter_by(user=user).order_by(Event.type.desc())
    if user_events.count() == 0:
        """First event, generate site visit"""
        generate_typed_event(event_type=Event.SITE_VISIT, user=user)
    else:
        """Generating next event in a row"""
        last_event = user_events.first()
        if last_event.type < Event.PURCHASE_CANCELLING:
            new_event = generate_typed_event(event_type=last_event.type + 1, user=user)
            if new_event.type == Event.PURCHASE_CANCELLING:
                """Purchase and its cancelling should have the same price"""
                new_metric = Metric.query.filter_by(event=new_event).one()
                old_metric = Metric.query.filter_by(event=last_event).one()
                new_metric.value = old_metric.value
                db.session.add(new_metric)
                db.session.commit()


def generate_typed_event(event_type: str, user: User) -> Event:
    """Generate one event of given type for given user"""
    event = Event(
        type=event_type,
        user=user,
        event_datetime=generate_time(),
    )

    """Saving event to database"""
    db.session.add(event)
    db.session.commit()

    match event_type:
        case Event.SITE_VISIT:
            event.source = random.choice(Event.SOURCE_TYPES)
            event.browser_type = random.choice(Event.BROWSER_TYPES)

            # В общем случае может быть более 1 метрики, поэтому лучше выписать все здесь
            metric = generate_metric(metric_type=Metric.PAGES_SCROLLED)
            metric.event = event

            db.session.add(metric)
            db.session.commit()

        case Event.PHONE_CALL:
            # Браузер и источник не определимы для звонка
            metric = generate_metric(metric_type=Metric.CALL_SUCCESS)
            metric.event = event

            db.session.add(metric)
            db.session.commit()

        case Event.PURCHASE:
            # Источник уже не определить, прошло время (Скорее всего. Ну а если нет, добавить просто)
            # event.browser_type = random.choice(Event.BROWSER_TYPES)

            metric = generate_metric(metric_type=Metric.PURCHASE_PRICE)
            metric.event = event

            db.session.add(metric)
            db.session.commit()

        case Event.PURCHASE_CANCELLING:
            # event.browser_type = random.choice(Event.BROWSER_TYPES)

            metric = generate_metric(metric_type=Metric.PURCHASE_PRICE)
            metric.event = event

            db.session.add(metric)
            db.session.commit()

    return event


def init_modeling():
    """Starts modeling and erases all created users and events"""
    User.drop()
    Metric.drop()
    Event.drop()

    user_count = random.randint(config.user_count_min, config.user_count_max)
    print(user_count)
    for i in range(user_count):
        generate_user()

    event_count = random.randint(config.event_count_min, config.event_count_max)
    print(event_count)
    for i in range(event_count):
        generate_event()

