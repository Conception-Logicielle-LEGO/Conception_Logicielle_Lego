"""
Business Objects et DTOs du projet LEGO Database Explorer

Organisation :
- Business Objects simples : Représentent les tables BDD 1:1
- DTOs enrichis : Résultats de JOINs SQL pour l'API (optimisation N+1)
"""

# ========== Core Entities (Catalogue DuckDB) ==========
# ========== DTOs Matching Algorithm (Fonctionnalité Phare) ==========
from .buildable_set import BuildableSet
from .color import Color
from .favorite_set import FavoriteSet
from .favorite_set_with_details import FavoriteSetWithDetails
from .missing_part import MissingPart

# ========== DTOs Enrichis (JOIN queries) ==========
from .part_with_details import PartWithDetails
from .set import Set
from .theme import Theme
from .user import User

# ========== User Data - PostgreSQL ==========
from .user_owned_set import UserOwnedSet, UserSetWithDetails
from .user_part import UserPart
from .wishlist import Wishlist
from .wishlist_part import WishlistPart
from .wishlist_part_with_details import WishlistPartWithDetails
from .wishlist_set import WishlistSet
from .wishlist_set_with_details import WishlistSetWithDetails


# Expose tout pour import facile : from business_object import User, BuildableSet
__all__ = [
    # Core Entities
    "User",
    "Set",
    "Color",
    "Theme",
    # User Data
    "UserOwnedSet",
    "UserSetWithDetails",
    "Wishlist",
    "WishlistPart",
    "WishlistSet",
    "FavoriteSet",
    "UserPart",
    # DTOs Enrichis
    "PartWithDetails",
    "WishlistPartWithDetails",
    "WishlistSetWithDetails",
    "FavoriteSetWithDetails",
    # DTOs Matching
    "BuildableSet",
    "MissingPart",
]
