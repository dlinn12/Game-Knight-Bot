from datetime import datetime, timedelta


class Saturday():
    """Wrapped DateTime obj with formatted tostring of month and day"""

    def __init__(self, dt):
        self.dt = dt

    def __str__(self):
        format_str = '%B %d'
        return self.dt.strftime(format_str)


def get_next_saturdays():
    d = datetime.today()
    wd = d.weekday()

    s1 = timedelta((12 - wd) % 7)
    s2 = timedelta((12 - wd) % 14)
    s3 = timedelta((19 - wd) % 21)
    s4 = timedelta((26 - wd) % 28)

    s1 = Saturday(d + s1)
    s2 = Saturday(d + s2)
    s3 = Saturday(d + s3)
    s4 = Saturday(d + s4)

    return s1, s2, s3, s4
