from pydantic import BaseModel


class AddWishlistSetBody(BaseModel):
    set_num: str
    priority: int = 0


class AddWishlistPartBody(BaseModel):
    part_num: str
    color_id: int
    quantity: int = 1


class UpdateWishlistPartQtyBody(BaseModel):
    quantity: int
