from datetime import datetime

from backend import *


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    events = db.relationship("Event", passive_deletes=True)

    @classmethod
    def drop(cls):
        """Remove all user objects"""
        try:
            db.session.query(cls).delete()
            db.session.commit()
        except:
            db.session.rollback()


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
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship("User", back_populates="events")
    event_datetime = db.Column(db.DateTime(), default=datetime.utcnow)
    metrics = db.relationship("Metric", passive_deletes=True)

    SOURCE_YANDEX = 'yandex'
    SOURCE_VK = 'vk'
    SOURCE_FACEBOOK = 'facebook'
    SOURCE_GOOGLE = 'google'

    SOURCE_TYPES = [
        SOURCE_YANDEX, SOURCE_VK, SOURCE_FACEBOOK, SOURCE_GOOGLE
    ]

    source = db.Column(db.String(100))

    BROWSER_DESKTOP = 'desktop'
    BROWSER_MOBILE = 'mobile'
    BROWSER_TABLET = 'tablet'
    BROWSER_TV = 'tv'

    BROWSER_TYPES = [
        BROWSER_DESKTOP, BROWSER_MOBILE, BROWSER_TABLET, BROWSER_TV
    ]

    browser_type = db.Column(db.String(100))

    @classmethod
    def get_event_types(cls):
        """Get all available event types"""
        return cls.TYPES

    @property
    def get_pretty_type(self) -> str:
        """Returns event type in human-readable way"""

        match self.type:
            case Event.SITE_VISIT:
                return 'site_visit'
            case Event.PHONE_CALL:
                return 'phone_call'
            case Event.PURCHASE:
                return 'purchase'
            case Event.PURCHASE_CANCELLING:
                return 'purchase_cancelling'

    def get_typed_metrics(self) -> dict:
        """Values of all available metrics"""
        data = {}
        for metric_type in Metric.get_metric_types():
            m_list = [m for m in self.metrics if m.type == metric_type]
            data[metric_type] = m_list[0].value if m_list else None
        # print(data)
        return data

    @classmethod
    def drop(cls):
        """Remove all event objects"""
        try:
            db.session.query(cls).delete()
            db.session.commit()
        except:
            db.session.rollback()


class Metric(db.Model):
    """Metric model"""

    PURCHASE_PRICE = 'purchase_price'
    PAGES_SCROLLED = 'pages_scrolled'
    CALL_SUCCESS = 'call_success'

    TYPES = [
        PURCHASE_PRICE, PAGES_SCROLLED, CALL_SUCCESS
    ]

    __tablename__ = 'metrics'

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    event_id = db.Column(db.Integer(), db.ForeignKey('events.id', ondelete='CASCADE'))
    event = db.relationship("Event", back_populates="metrics")

    value = db.Column(db.Integer(), nullable=False)

    @classmethod
    def get_metric_types(cls):
        """Returns all metrics types"""
        return cls.TYPES

    @classmethod
    def drop(cls):
        """Remove all event objects"""
        try:
            db.session.query(cls).delete()
            db.session.commit()
        except:
            db.session.rollback()
