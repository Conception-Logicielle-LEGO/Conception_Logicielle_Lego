from pydantic import BaseModel


class RegisterBody(BaseModel):
    username: str
    password: str


class LoginBody(BaseModel):
    username: str
    password: str


class ChangePasswordBody(BaseModel):
    old_password: str
    new_password: str


class ChangeUsernameBody(BaseModel):
    new_username: str
