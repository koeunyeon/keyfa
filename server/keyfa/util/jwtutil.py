from datetime import datetime
import jwt

from config import Config
from keyfa.util import dateutil


def encode(**data: dict) -> str:
    payload = data
    payload["exp"] = dateutil.add(
        std_dt = datetime.now(),
        days=Config.jwt.expired_days, 
        seconds=Config.jwt.expired_seconds,
        minutes=Config.jwt.expired_minutes,
        hours=Config.jwt.expired_hours,
        weeks=Config.jwt.expired_weeks
    )
    
    token = jwt.encode(payload, key=Config.jwt.secret, algorithm=Config.jwt.algorithm)        
    return token

def decode(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, key=Config.jwt.secret, algorithms=[Config.jwt.algorithm])        
        exp = datetime.utcfromtimestamp(decode_token["exp"])
        return decode_token if dateutil.is_not_over(exp) else {}
    except Exception as ex:        
        return {}