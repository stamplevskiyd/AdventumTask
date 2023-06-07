from backend import db, models


def save_object(obj) -> None:
    """Save obj to db"""
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to save object due to {e}")


def find_last_event(user: models.User) -> models.Event:
    """Finds last event for this user"""
    event = models.Event.query.filter_by(user=user).order_by(models.Event.type.desc()).first()
    return event


def find_event_by_type(user: models.User, event_type: int) -> models.Event:
    """Find event of given tipe for given user"""
    event = models.Event.query.filter_by(user=user).filter_by(type=event_type).order_by(models.Event.type.desc()).first()
    return event


def find_last_event_type(user: models.User) -> int:
    """Finds type of last user's event"""
    event = models.Event.query.filter_by(user=user).order_by(models.Event.type.desc()).first()
    return event.type if event else 0


def clear_table(model) -> None:
    """Clear table for given model"""
    try:
        db.session.query(model).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Failed to drop {model.__tablename__} due to {e}")


def clear_db() -> None:
    """Drop all tables to start new modeling"""
    for model in [models.Event, models.Metric, models.User]:
        clear_table(model)
