from pydantic import BaseModel


class AddSetBody(BaseModel):
    set_num: str
    is_built: bool = False


class UpdateBuiltBody(BaseModel):
    is_built: bool
