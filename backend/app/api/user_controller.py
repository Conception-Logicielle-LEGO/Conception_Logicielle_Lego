from database.connexion import db_connection
from database.dao.user_dao import UserDAO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.user_service import UserService
import uvicorn


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


def run_app():
    """
    Starts the FastAPI application using Uvicorn.
    - Runs on host 0.0.0.0 (accessible from outside container)
    - Port 8000
    - Reload enabled for development
    """
    uvicorn.run(
        "backend.app.api.user_controller:app", host="0.0.0.0", port=8000, reload=True
    )


@app.post("/create_user")
async def create_user(username: str, password: str):
    userdao = UserDAO(db_connection=db_connection(read_only=False))
    userservice = UserService(user_dao=userdao)
    user = userservice.create_user(username=username, password=password)

    if user is None:
        raise Exception(status_code=409, detail="Unable to create user")

    return "account created"


@app.get("/owned_parts")
async def get_owned_parts(username: str):
    userdao = UserDAO(db_connection=db_connection(read_only=True))

    users = userdao.get_by(column="username", value=username)
    if users is None:
        raise Exception(status_code=404, detail="unable to find user")

    user = users[0]
    id_user = user.id_user

    result = userdao.get_owned_parts(id_user=id_user)

    # éventuellement mettre en forme le résultat mais ça dépend du format retenu
    return result


@app.put("/change_password")
async def change_password(username: str, old_password: str, new_password: str):
    userdao = UserDAO(db_connection=db_connection(read_only=False))
    userservice = UserService(user_dao=userdao)

    success = userservice.change_password(
        username=username, old_password=old_password, new_password=new_password
    )

    if not success:
        raise Exception(detail="unable to change password")

    else:
        return "Mot de passe changé avec succès"
