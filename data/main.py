from .selector_strategy.rulebase import hitstock
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.tz import tzlocal

if __name__ == "__main__":
    from_zone = tz.gettz(datetime.now(tzlocal()).tzname())
    to_zone = tz.gettz('CST')
    today = datetime.today().replace(tzinfo=from_zone).astimezone(to_zone)
    if today.weekday() < 5:
        last_day = (today - timedelta(days=1)).strftime('%Y%m%d')
        today = today.strftime('%Y%m%d')
        hitstock(last_day, today)
    else:
        print('No Data Because of Weekends')
