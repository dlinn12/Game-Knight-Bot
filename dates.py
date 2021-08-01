from datetime import datetime, timedelta


class Saturday():
    """Wrapped DateTime obj with formatted tostring of month and day"""

    def __init__(self, dt):
        self.dt = dt

    def __str__(self):
        format_str = '%B %d'
        return self.dt.strftime(format_str)


def get_next_saturdays():
    date = datetime.today()
    s = 5
    # each consequent sat. is 7,14, and 21 days ahead
    days_ahead = s - date.weekday()
    if days_ahead <= 0:  # currently saturday or sunday
        days_ahead += 7

    s1 = Saturday(date + timedelta(days_ahead))
    s2 = Saturday(date + timedelta(days_ahead + 7))
    s3 = Saturday(date + timedelta(days_ahead + 14))
    s4 = Saturday(date + timedelta(days_ahead + 21))
    return s1, s2, s3, s4
