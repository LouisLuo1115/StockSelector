from datetime import datetime, timedelta
from dateutil import tz
from dateutil.tz import tzlocal

def timezone_handler(timestamp, timezone='CST'):
    from_zone = tz.gettz(datetime.now(tzlocal()).tzname())
    to_zone = tz.gettz(timezone)
    timestamp = timestamp.replace(tzinfo=from_zone).astimezone(to_zone)

    return timestamp

def get_stock_date_handler(timestamp):
    if timestamp.time < datetime.strptime('18:30',"%H:%M").time():
        timestamp = timestamp - timedelta(days=1)
        
    if timestamp.weekday() < 5:
        timestamp = timestamp.strftime('%Y%m%d')
    else:
        delta = timestamp.weekday - 4
        timestamp = (timestamp - timedelta(days=delta)).strftime('%Y%m%d')
    
    return timestamp
