from sqlalchemy.orm import Session  # type: ignore
from fastapi import HTTPException

from .schemas import UserLogin
from common.models import UserModel
from . exceptions import user_not_exist_exception, email_exist_exception

def get_user_from_id(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user:
        return user
    else:
        raise user_not_exist_exception

def check_for_user_email(db: Session, email):
    return db.query(UserModel).filter(UserModel.email == email).first()


def validate_user(db: Session, user: UserLogin):
    return db.query(UserModel).filter(UserModel.email == user.email, UserModel.password == user.password).first()


def add_user(db: Session, user):
    if check_for_user_email(db, user.email):
        raise email_exist_exception
    db_user = UserModel(email=user.email, first_name=user.first_name,
                        last_name=user.last_name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def add_google_user(db: Session, user):

    if check_for_user_email(db, user.email):
        raise HTTPException(
            detail="Email already registered", status_code=409
        )
    db_user = UserModel(
        email=user.email, first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
