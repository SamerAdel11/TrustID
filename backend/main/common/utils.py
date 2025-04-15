import jwt

from user.auth.services import JWT_ALGORITHM, JWT_SECRET_KEY

def pydantic_to_dict(model):
    return {attr: getattr(model, attr) for attr in model.__dict__}


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
