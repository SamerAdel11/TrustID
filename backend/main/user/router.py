from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv # type: ignore
from requests import Session

from .crud import add_user, get_user_from_id
from .schemas import *
from .auth.services import *
from common.utils import pydantic_to_dict
from common.database import get_db

user_router = APIRouter()
load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="add_user")


@user_router.post("/")
def add_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    user_data = add_user(db=db, user=user)
    return get_access_and_refresh_token(pydantic_to_dict(user_data))


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user_from_id(db=db, user_id=user_id)
