from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from requests import Session

from user.crud import validate_user
from user.schemas import *
from user.auth import services
from user.exceptions import token_invalid_exception, user_not_exist_exception

from common.utils import pydantic_to_dict, decode_jwt
from common.database import get_db

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="add_user")

@auth_router.post("/login")
def login_endpoint(user: UserLogin, db: Session = Depends(get_db)):
    user = validate_user(db, user)
    if user:
        tokens = services.get_access_and_refresh_token(pydantic_to_dict(user))
        return JSONResponse(tokens)
    else:
        raise user_not_exist_exception

@auth_router.post("/refresh")
async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = decode_jwt(token)
        return services.get_access_and_refresh_token(payload)
    except InvalidTokenError:
        raise token_invalid_exception