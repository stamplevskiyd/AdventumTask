import datetime
import random

from backend.models import Event, User, Metric
from backend import db


def generate_event() -> None:
    """Generate one random event and all required
    (third type generates also second and first)
    """

    event_type = random.choice(Event.get_event_types())
    user = random.choice(User.query.all())

    match event_type:
        case Event.SITE_VISIT:
            generate_typed_event(event_type=Event.SITE_VISIT, user=user)
        case Event.PHONE_CALL:
            generate_typed_event(event_type=Event.SITE_VISIT, user=user)
            generate_typed_event(event_type=Event.PHONE_CALL, user=user)
        case Event.PURCHASE:
            generate_typed_event(event_type=Event.SITE_VISIT, user=user)
            generate_typed_event(event_type=Event.PHONE_CALL, user=user)
            generate_typed_event(event_type=Event.PURCHASE, user=user)
        case Event.PURCHASE_CANCELLING:
            generate_typed_event(event_type=Event.SITE_VISIT, user=user)
            generate_typed_event(event_type=Event.PHONE_CALL, user=user)
            generate_typed_event(event_type=Event.PURCHASE, user=user)
            generate_typed_event(event_type=Event.PURCHASE_CANCELLING, user=user)


def generate_typed_event(event_type: str, user: User) -> None:
    """Generate one event of given type for given user"""

    event = Event(
        type=event_type,
        user=user,
        event_datetime=datetime.datetime.now(),  # TODO: заглушка
    )

    """Saving event to database"""
    db.session.add(event)
    db.session.commit()

    metric = Metric(
        event=event
    )

    match event_type:
        case Event.SITE_VISIT:
            metric.type = Metric.PAGES_SCROLLED
            metric.value = random.randint(1, 1000)  # TODO: заглушка
            event.source = random.choice(Event.SOURCE_TYPES)
            event.browser_type = random.choice(Event.BROWSER_TYPES)
        case Event.PHONE_CALL:
            metric.type = Metric.CALL_SUCCESS
            metric.value = random.randint(1, 1000)  # TODO: заглушка
            # Браузер и источник не определимы для звонка
        case Event.PURCHASE:
            metric.type = Metric.PURCHASE_PRICE
            metric.value = random.randint(1, 1000)  # TODO: заглушка
            # event.source = random.choice(Event.SOURCE_TYPES)
            event.browser_type = random.choice(Event.BROWSER_TYPES)
        case Event.PURCHASE_CANCELLING:
            metric.type = Metric.PURCHASE_PRICE
            metric.value = random.randint(1, 1000)  # TODO: заглушка
            # event.source = random.choice(Event.SOURCE_TYPES)
            event.browser_type = random.choice(Event.BROWSER_TYPES)

    """Saving event and metric to database"""
    db.session.add(metric)
    db.session.add(event)
    db.session.commit()
