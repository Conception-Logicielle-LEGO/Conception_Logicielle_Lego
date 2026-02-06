from database.connexion import db_connection
from database.dao.user_dao import UserDAO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.user_service import UserService


# Instantiate the web service
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/user/get_user")
async def create_user(username: str, password: str):
    userdao = UserDAO(db_connection=db_connection(read_only=False))
    userservice = UserService(user_dao=userdao)
    user = userservice.create_user(username=username, password=password)

    if user is None:
        raise Exception(status_code=409, detail="Unable to create user")

    return "account created"
