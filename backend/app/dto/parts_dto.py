from pydantic import BaseModel


class AddPartBody(BaseModel):
    part_num: str
    color_id: int = 0
    quantity: int = 1
    is_used: bool = False


class UpdatePartQtyBody(BaseModel):
    quantity: int
    is_used: bool = False
