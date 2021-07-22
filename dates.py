from datetime import datetime, timedelta


def get_next_saturdays():
    format_str = '%B %d'
    d = datetime.today()
    wd = d.weekday()

    s1 = timedelta((12 - wd) % 7)
    s2 = timedelta((12 - wd) % 14)
    s3 = timedelta((19 - wd) % 21)
    s4 = timedelta((26 - wd) % 28)

    s1 = (d + s1).strftime(format_str)
    s2 = (d + s2).strftime(format_str)
    s3 = (d + s3).strftime(format_str)
    s4 = (d + s4).strftime(format_str)

    return s1, s2, s3, s4
