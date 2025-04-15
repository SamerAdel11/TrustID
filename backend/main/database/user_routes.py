# from fastapi import APIRouter, Depends, Request,HTTPException, status, Response
# from sqlalchemy.orm import Session
# from fastapi.responses import RedirectResponse, JSONResponse,HTMLResponse
# import requests
# import os
# from dotenv import load_dotenv
# import datetime
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# # from jose import JWTError, jwt
# from datetime import datetime, timedelta,timezone
# from typing import Optional,Annotated
# import jwt
# from jwt.exceptions import InvalidTokenError

# from .schemas import UserLogin, UserResponse, UserCreate, GoogleUserCreate
# from ..auth.crud import get_user_from_id, add_user, add_google_user, check_for_user_email, validate_user
# from ..database import get_db
# import services
# api_router= APIRouter()

# load_dotenv()
# # Google OAuth2 Credentials
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# # Google OAuth2 URLs
# GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
# GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
# GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# # JWT Tokens
# JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
# JWT_ALGORITHM='HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES=30
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="add_user")

# @api_router.get("/user_data",response_model=UserResponse)
# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:Session=Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     # print("Token is ",token)
#     # try:
#     payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
#     # except InvalidTokenError:
#     #     raise credentials_exception
#     user = check_for_user_email(db=db, email=payload['email'])
#     if user is None:
#         print("user not found")
#         raise credentials_exception
#     return user

# @api_router.get("/token/refresh")
# async def refresh_token(token: Annotated[str, Depends(oauth2_scheme)], db:Session=Depends(get_db)):
#     credentials_exception = HTTPException(
# status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Could not validate credentials",
#     headers={"WWW-Authenticate": "Bearer"},
#     )
#     print("token is,",token," and it's type is ",type(token))
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
#         print("payload is ",payload)
#         return get_access_and_refresh_token(payload)
#     except InvalidTokenError:
#         raise credentials_exception

# @api_router.get("/google_auth",response_class=HTMLResponse)
# async def home():
#     """Step 1: Show Login Button"""
#     google_login_url = (
#         f"{GOOGLE_AUTH_URL}?response_type=code"
#         f"&client_id={GOOGLE_CLIENT_ID}"
#         f"&redirect_uri={GOOGLE_REDIRECT_URI}"
#         f"&scope=email%20profile"
#         f"&access_type=offline"
#         f"&prompt=consent"

#     )
#     return JSONResponse({"auth_url": google_login_url})


# @api_router.get("/callback")
# async def callback(request: Request,db: Session= Depends(get_db)):
#     """Step 2: Receive Authorization Code & Request Access Token"""
#     print("Call back is being called")
#     code = request.query_params.get("code")
#     if not code:
#         return JSONResponse({"error": "No code received"}, status_code=400)
#     return get_google_tokens(code,db)
#     return RedirectResponse('/home')
#     #  

# def get_google_tokens(code,db):
#     # Step 3: Exchange Authorization Code for Access Token
#     response = requests.post(
#         GOOGLE_TOKEN_URL,
#         data={
#             "code": code,
#             "client_id": GOOGLE_CLIENT_ID,
#             "client_secret": GOOGLE_CLIENT_SECRET,
#             "redirect_uri": GOOGLE_REDIRECT_URI,
#             "grant_type": "authorization_code",
#         },
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#     )

#     token_data = response.json()
#     if "access_token" not in token_data:
#         return JSONResponse({"detail":"Response Doesn't have access_token",
#                             "Tokens": token_data}, status_code=400)
#     return get_google_user_info(token_data,db)

# def get_google_user_info(google_tokens,db):
#     google_access_token = google_tokens["access_token"]

#     # Step 4: Fetch User Info
#     user_info_response = requests.get(
#         GOOGLE_USERINFO_URL,
#         headers={"Authorization": f"Bearer {google_access_token}"},
#     )
#     user_info = user_info_response.json()

#     first_name=user_info.get('given_name')
#     last_name=user_info.get('family_name')
#     email=user_info.get('email')

#     user_data=add_google_user(db=db,user=GoogleUserCreate(first_name=first_name,
#                 last_name=last_name,email=email))

#     # access_token=create_token(user_data,expire_time=timedelta(minutes=30))
#     # refresh_token=create_token(user_data,expire_time=timedelta(days=7))
#     return get_access_and_refresh_token(pydantic_to_dict(user_data))


# @api_router.post("/user")
# def add_user_endpoint( user: UserCreate, db: Session= Depends(get_db)):
#     user_data=add_user(db=db,user=user)
#     return get_access_and_refresh_token(pydantic_to_dict(user_data))

# @api_router.post("/auth/login")
# def login_endpoint(user: UserLogin, db: Session=Depends(get_db)):
#     user = validate_user(db,user)
#     if user:
#         tokens=services.get_access_and_refresh_token(pydantic_to_dict(user))
#         # response.set_cookie(key="access_token", value=tokens.get('access_token'))
#         # response.set_cookie(key="refresh_token", value=tokens.get('refresh_token'))
#         return JSONResponse(tokens)
#     else:
#         raise HTTPException(detail="No user with this credintials",status_code=404)

# @api_router.get("/is_authenticated")
# async def is_authenticated(request: Request):
#     token = request.cookies.get("access_token")
#     return JSONResponse({"authenticated": bool(token)})

# @api_router.get("/users/{user_id}",response_model=UserResponse)
# def get_user_endpoint(user_id: int ,db: Session = Depends(get_db)):
#     return get_user_from_id(db=db, user_id=user_id)

# def pydantic_to_dict(model):
#     return {attr: getattr(model, attr) for attr in model.__dict__}
