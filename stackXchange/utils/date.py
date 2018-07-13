from datetime import (
    datetime,
    timedelta
)


def epoch_to_datetime(epochtime):
    return datetime.fromtimestamp(epochtime)


def add_days_to_today(days):
    return datetime.today() + timedelta(days=days)
