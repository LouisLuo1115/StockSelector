from .selector_strategy.rulebase import hitstock
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.tz import tzlocal

from ..utilitylib.time_handler import timezone_handler

if __name__ == "__main__":
    today = timezone_handler(datetime.today())
    if today.weekday() in [1, 2, 3, 4]:
        last_day = (today - timedelta(days=1)).strftime('%Y%m%d')
        today = today.strftime('%Y%m%d')
        hitstock(last_day, today)
    elif today.weekday() == 0:
        last_day = (today - timedelta(days=3)).strftime('%Y%m%d')
        today = today.strftime('%Y%m%d')
        hitstock(last_day, today)   
    else:
        print('No Data Because of Weekends')
