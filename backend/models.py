from datetime import datetime

from backend import *


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    events = db.relationship("Event", passive_deletes=True)

    def get_last_event(self):
        """Get last user event"""
        return max(self.events, key=lambda x: x.type)


class Event(db.Model):
    """Event model"""

    __tablename__ = 'events'
    id = db.Column(db.Integer(), primary_key=True)

    SITE_VISIT = 1
    PHONE_CALL = 2
    PURCHASE = 3
    PURCHASE_CANCELLING = 4

    TYPES = [
        SITE_VISIT, PHONE_CALL, PURCHASE, PURCHASE_CANCELLING
    ]
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

    BROWSER_TYPES = [
        BROWSER_DESKTOP, BROWSER_MOBILE, BROWSER_TABLET
    ]
    browser_type = db.Column(db.String(100))

    def get_pretty_type(self):
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

    def get_typed_metrics(self):
        """Values of all available metrics"""
        data = {}
        for metric_type in Metric.TYPES:
            m_list = [m for m in self.metrics if m.type == metric_type]
            data[metric_type] = m_list[0].value if m_list else None
        return data


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
