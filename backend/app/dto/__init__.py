from pydantic import BaseModel


class AddSetBody(BaseModel):
    set_num: str
    is_built: bool = False


class UpdateBuiltBody(BaseModel):
    is_built: bool


class AddPartBody(BaseModel):
    part_num: str
    color_id: int = 0
    quantity: int = 1
    is_used: bool = False


class UpdatePartQtyBody(BaseModel):
    quantity: int
    is_used: bool = False


class AddWishlistSetBody(BaseModel):
    set_num: str
    priority: int = 0


class AddWishlistPartBody(BaseModel):
    part_num: str
    color_id: int
    quantity: int = 1


class UpdateWishlistPartQtyBody(BaseModel):
    quantity: int


class AddFavoriteBody(BaseModel):
    set_num: str


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
