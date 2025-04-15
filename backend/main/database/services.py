# from datetime import datetime, timedelta,timezone
# from typing import Optional,Annotated
# import jwt
# import os

# JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
# JWT_ALGORITHM='HS256'

# def create_token(data: dict,type:str, expire_time: Optional[timedelta] = None):
#     to_encode = {
#         "sub":str(data.get('id')) or str(data.sub),
#         "email":str(data.get('email')) or str(data.email),
#         "iat":datetime.now(timezone.utc),
#         "exp": datetime.now(timezone.utc) +( expire_time if expire_time else timedelta(minutes=20))
#     }
#     if type=='access':
#         to_encode.update({"first_name":str(data.get('first_name')) or str(data.first_name)})
#         to_encode.update({"role":'user'})
#     return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

# def get_access_and_refresh_token(user_data):
#     return {"access_token":create_token(user_data, type='access',expire_time=timedelta(minutes=30)),
#             "refresh_token":create_token(user_data,type='refresh',expire_time=timedelta(days=7))}