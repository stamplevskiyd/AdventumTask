import datetime
import random
import names

from backend import db_functions, config, models

current_time = datetime.datetime.now()


def get_time() -> datetime.datetime:
    """Generates sequential random time"""
    global current_time
    current_time += datetime.timedelta(seconds=random.randint(1, 1000))
    return current_time


def generate_event() -> None:
    """Generates event of random type.
    Creates new user for site visit, chooses suitable user for other types
    """
    available_types = [
        i for i in
        set([1] + [db_functions.find_last_event_type(user) + 1 for user in models.User.query.all()])
        if i <= models.Event.PURCHASE_CANCELLING
    ]
    event_type = random.choice(available_types)

    if event_type == models.Event.SITE_VISIT:
        user = models.User(name=names.get_full_name())
        db_functions.save_object(user)
    else:
        # Пользователи, для которых применимо событие данного типа
        suitable_users = [
            user for user in models.User.query.all()
            if (event := db_functions.find_last_event(user)) is not None and event.type == event_type - 1
        ]  # Их существование гарантирует логика выбора типа события в предыдущем коде
        user = random.choice(suitable_users)

    event = models.Event(
        type=event_type,
        user=user,
        event_datetime=get_time(),
    )

    if event_type == models.Event.SITE_VISIT:
        event.source = random.choice(models.Event.SOURCE_TYPES)
        event.browser_type = random.choice(models.Event.BROWSER_TYPES)

    db_functions.save_object(event)
    generate_metrics(event=event)


def generate_metrics(event: models.Event) -> None:
    """Generate all needed metrics for given event"""
    metrics = []
    print("EVENT", event, event.id)
    match event.type:
        case models.Event.SITE_VISIT:
            # В общем случае может быть более 1 метрики, поэтому лучше выписать все здесь
            metric = models.Metric(type=models.Metric.PAGES_SCROLLED)
            metric.value = random.randint(config.pages_scrolled_min, config.pages_scrolled_max)
            metrics.append(metric)
        case models.Event.PHONE_CALL:
            # Браузер и источник не определимы для звонка
            metric = models.Metric(type=models.Metric.CALL_SUCCESS)
            metric.value = random.randint(config.call_success_min, config.call_success_max)
            metrics.append(metric)
        case models.Event.PURCHASE:
            metric = models.Metric(type=models.Metric.PURCHASE_PRICE)
            metric.value = random.randint(config.purchase_price_min, config.purchase_price_max)
            metrics.append(metric)
        case models.Event.PURCHASE_CANCELLING:
            metric = models.Metric(type=models.Metric.PURCHASE_PRICE)
            prev_event = db_functions.find_event_by_type(user=event.user, event_type=models.Event.PURCHASE)
            print("PREV_EVENT", prev_event)
            print("PREV_METRIC", prev_event.metrics)
            price = [m for m in prev_event.metrics if m.type == models.Metric.PURCHASE_PRICE][0].value
            metric.value = price
            metrics.append(metric)

    """Saving all generated metrics"""
    for m in metrics:
        m.event = event
        db_functions.save_object(m)


def init_modeling() -> None:
    """Starts modeling and erases all created users and events"""

    db_functions.clear_db()

    event_count = random.randint(config.event_count_min, config.event_count_max)
    for i in range(event_count):
        generate_event()
