"""
DTO pour l'algorithme de matching des sets réalisables
Fonctionnalité principale du projet
"""

from dataclasses import dataclass


@dataclass
class BuildableSet:
    """
    DTO pour l'algorithme de matching.
    Représente un set avec son pourcentage de réalisabilité
    basé sur les pièces possédées par l'utilisateur.

    Utilisé par MatchingService pour retourner:
    - Sets 100% réalisables
    - Sets "presque réalisables" (ex: 80%+)
    - Pièces manquantes pour compléter un set
    """

    # Données du set (catalogue)
    set_num: str
    name: str
    year: int
    theme_id: int
    num_parts: int

    # Statistiques de matching
    total_parts_needed: int  # Nombre total de pièces uniques nécessaires
    parts_owned: int  # Nombre de pièces uniques possédées
    completion_percentage: float  # % de pièces possédées (0-100)

    # Détails des pièces manquantes
    missing_parts_count: int  # Nombre de pièces uniques manquantes

    # Champs optionnels (avec valeur par défaut — doivent être en dernier)
    img_url: str | None = None
    missing_parts: list[dict] | None = None  # Liste détaillée (optionnel)

    def __str__(self) -> str:
        icon = "✅" if self.is_buildable() else "🔨"
        return (
            f"{icon} {self.name} ({self.set_num}) - "
            f"{self.completion_percentage:.0f}% réalisable "
            f"({self.parts_owned}/{self.total_parts_needed} pièces)"
        )

    @classmethod
    def from_dict(cls, data: dict):
        """Créer depuis un résultat de calcul SQL"""
        return cls(
            # Set info
            set_num=data["set_num"],
            name=data["name"],
            year=data["year"],
            theme_id=data["theme_id"],
            num_parts=data["num_parts"],
            img_url=data.get("img_url"),
            # Matching stats
            total_parts_needed=data["total_parts_needed"],
            parts_owned=data["parts_owned"],
            completion_percentage=data["completion_percentage"],
            missing_parts_count=data["missing_parts_count"],
            missing_parts=data.get("missing_parts"),
        )

    def to_dict(self) -> dict:
        """Pour JSON API"""
        result = {
            "set": {
                "set_num": self.set_num,
                "name": self.name,
                "year": self.year,
                "theme_id": self.theme_id,
                "num_parts": self.num_parts,
                "img_url": self.img_url,
            },
            "buildability": {
                "is_buildable": self.is_buildable(),
                "completion_percentage": round(self.completion_percentage, 2),
                "parts_owned": self.parts_owned,
                "total_parts_needed": self.total_parts_needed,
                "missing_parts_count": self.missing_parts_count,
            },
        }

        # Ajouter les détails des pièces manquantes si disponibles
        if self.missing_parts:
            result["missing_parts"] = self.missing_parts

        return result

    def is_buildable(self) -> bool:
        """Vérifie si le set est 100% réalisable"""
        return self.completion_percentage >= 100.0

    def is_almost_buildable(self, threshold: float = 80.0) -> bool:
        """Vérifie si le set est presque réalisable (>= threshold%)"""
        return self.completion_percentage >= threshold

    def get_priority_score(self) -> float:
        """
        Calcule un score de priorité pour trier les sets.
        Privilégie les sets presque complets avec peu de pièces manquantes.

        Formule: completion_percentage * (1 - missing_parts_count/100)
        """
        if self.is_buildable():
            return 100.0

        # Pénaliser les sets avec beaucoup de pièces manquantes
        penalty = min(self.missing_parts_count / 100, 0.5)
        return self.completion_percentage * (1 - penalty)
