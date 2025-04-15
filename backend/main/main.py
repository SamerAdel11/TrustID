from fastapi import FastAPI
import uvicorn  # type: ignore
from fastapi.middleware.cors import CORSMiddleware

from common.database import Base, engine
from user.router import user_router
from user.auth.router import auth_router

app = FastAPI()
origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Only allow frontend from port 3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(user_router, prefix="/user")
app.include_router(auth_router, prefix="/auth")

if __name__ == '__main__':
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="127.0.0.1", port=9000)
