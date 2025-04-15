from datetime import datetime, timedelta,timezone
from typing import Optional,Annotated
import jwt
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()
JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM ='HS256'

def create_token(data: dict, token_type: str, expire_time: Optional[timedelta] = None):
    # Handle both dict and object-like access
    def get_value(key, default=None):
        if isinstance(data, dict):
            return data.get(key, default)
        return getattr(data, key, default)
    now=datetime.now(timezone.utc)
    to_encode = {
        "sub": str(get_value('id')),
        "email": str(get_value('email')),
        "iat": now,
        "exp": now + (expire_time if expire_time else timedelta(minutes=20))
    }

    if token_type == 'access':
        to_encode.update({"first_name": str(get_value('first_name')),
                            "role": 'user'})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_access_and_refresh_token(user_data):
    return {"access_token":create_token(user_data, token_type='access',expire_time=timedelta(seconds=30)),
            "refresh_token":create_token(user_data,token_type='refresh',expire_time=timedelta(days=7))}