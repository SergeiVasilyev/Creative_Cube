import pytz
from datetime import datetime, timedelta
from .models import *



def datetime_now() -> datetime:
    now = datetime.now()
    datenow = pytz.utc.localize(now)
    return datenow


def order_details(orderID):
    order = Order.objects.get(transaction_id=orderID)


def create_slug(text) -> str:
    text = str(text.lower())
    slug = text.replace(' ', '_')
    return slug