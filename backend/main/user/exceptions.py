from fastapi import HTTPException, status

token_invalid_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
    )
user_not_exist_exception = HTTPException(
            detail="No user with this credintials",
            status_code=404)
email_exist_exception=HTTPException(
            detail="Email already registered", status_code=409
        )