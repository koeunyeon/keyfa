from datetime import datetime, timedelta

def add(std_dt: datetime = datetime.now(), 
        days=0, seconds=0, microseconds=0,
        milliseconds=0, minutes=0, hours=0, weeks=0):
        return std_dt + timedelta(
                days=days, seconds=seconds, microseconds=microseconds, 
                milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

def is_over(diff_date: datetime,
            std_dt: datetime = datetime.now()):
            
        return std_dt > diff_date

def is_not_over(diff_date: datetime,
            std_dt: datetime = datetime.now()):
    return not is_over(diff_date, std_dt)