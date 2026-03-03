from pydantic import BaseModel


class AddFavoriteBody(BaseModel):
    set_num: str
