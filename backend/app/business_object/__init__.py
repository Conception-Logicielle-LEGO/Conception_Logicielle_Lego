"""
Business Objects du projet LEGO Database Explorer

Organisation :
- Business Objects simples : Représentent les tables BDD 1:1
- DTOs algorithme : Résultats du matching sets constructibles
"""

# ========== Catalogue DuckDB ==========
# ========== DTOs algorithme de matching ==========
from .buildable_set import BuildableSet
from .color import Color
from .favorite_set import FavoriteSet
from .missing_part import MissingPart
from .set import Set
from .theme import Theme

# ========== User Data - PostgreSQL ==========
from .user import User
from .user_owned_set import UserOwnedSet
from .user_part import UserPart
from .wishlist import Wishlist
from .wishlist_part import WishlistPart
from .wishlist_set import WishlistSet


__all__ = [
    # Catalogue
    "Color",
    "Set",
    "Theme",
    # User Data
    "User",
    "UserOwnedSet",
    "UserPart",
    "Wishlist",
    "WishlistPart",
    "WishlistSet",
    "FavoriteSet",
    # DTOs Matching
    "BuildableSet",
    "MissingPart",
]
