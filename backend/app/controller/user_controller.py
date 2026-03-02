from fastapi import APIRouter, HTTPException

from app.api.dependencies import PgDep
from app.database.dao.user_dao import UserDAO
from app.dto import ChangePasswordBody, ChangeUsernameBody, LoginBody, RegisterBody
from app.service.password_service import PasswordService
from app.service.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=201)
def register(body: RegisterBody, pg: PgDep):
    dao = UserDAO(pg)
    if dao.is_username_taken(body.username):
        raise HTTPException(status_code=409, detail="Username déjà pris")
    result = UserService(dao).create_user(body.username, body.password)
    if result is None:
        raise HTTPException(
            status_code=500, detail="Erreur lors de la création du compte"
        )
    pg.commit()
    return {"id_user": result.id_user, "username": result.username}


@router.post("/login")
def login(body: LoginBody, pg: PgDep):
    dao = UserDAO(pg)
    try:
        user = PasswordService(dao).validate_username_password(
            body.username, body.password
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    return {"id_user": user.id_user, "username": user.username}


@router.put("/{user_id}/password")
def change_password(user_id: int, body: ChangePasswordBody, pg: PgDep):
    dao = UserDAO(pg)
    user = dao.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    ok = UserService(dao).change_password(
        user.username, body.old_password, body.new_password
    )
    if not ok:
        raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect")
    pg.commit()
    return {"detail": "Mot de passe mis à jour"}


@router.put("/{user_id}/username")
def change_username(user_id: int, body: ChangeUsernameBody, pg: PgDep):
    dao = UserDAO(pg)
    user = dao.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    ok = UserService(dao).change_username(user.username, body.new_username)
    if not ok:
        raise HTTPException(status_code=409, detail="Username déjà pris")
    pg.commit()
    return {"detail": "Username mis à jour"}
