from backend import *


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    events = db.relationship("Event")


class Event(db.Model):
    """Event model"""

    SITE_VISIT = 1
    PHONE_CALL = 2
    PURCHASE = 3
    PURCHASE_CANCELLING = 4

    TYPES = [
        SITE_VISIT, PHONE_CALL, PURCHASE, PURCHASE_CANCELLING
    ]

    __tablename__ = 'events'

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer(), nullable=False)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="events")

    metrics = db.relationship("Metric")

    @classmethod
    def get_event_types(cls):
        """Get all available event types"""
        return cls.TYPES


class Metric(db.Model):
    """Metric model"""

    PURCHASE_PRICE = 1
    PAGES_SCROLLED = 2
    CALL_SUCCESS = 3

    TYPES = [
        PURCHASE_PRICE, PAGES_SCROLLED, CALL_SUCCESS
    ]

    __tablename__ = 'metrics'

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer(), nullable=False)

    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
    event = db.relationship("Event", back_populates="metrics")

    @classmethod
    def get_metric_types(cls):
        """Returns all metrics types"""
        return cls.TYPES
