"""
Génération des embeddings pour la recherche sémantique VSS dans DuckDB.

Peut être appelé de deux façons :
  1. Directement : python app/database/duckdb/generate_embeddings.py
  2. Via init_db_lego.py (appelé automatiquement si sentence-transformers est installé)

Textes encodés :
  - Sets  : "{name} {theme_name}"  → ex. "Millennium Falcon Star Wars"
  - Parts : "{name} {category_name}" → ex. "Brick 2x4 Bricks"

Modèle : all-MiniLM-L6-v2 (384 dimensions, rapide et léger)
Index  : HNSW via extension DuckDB VSS
"""

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import duckdb
from fastembed import TextEmbedding

from app.database.connexion_duckdb import DB_PATH


BATCH_SIZE = 500
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DIMS = 384


def generate_embeddings(conn: duckdb.DuckDBPyConnection | None = None) -> None:
    """Génère les embeddings et les indexes HNSW dans la base DuckDB.

    Args:
        conn: Connexion DuckDB ouverte en écriture.
              Si None, ouvre DB_PATH en écriture (usage standalone).
    """
    standalone = conn is None
    if standalone:
        if not DB_PATH.exists():
            print(f"Erreur : base DuckDB introuvable : {DB_PATH}")
            sys.exit(1)
        print(f"Ouverture de {DB_PATH} en écriture...")
        conn = duckdb.connect(str(DB_PATH), read_only=False)

    try:
        print("Chargement de l'extension VSS...")
        conn.execute("INSTALL vss")
        conn.execute("LOAD vss")
        conn.execute("SET hnsw_enable_experimental_persistence = true")

        print(f"Chargement du modèle {MODEL_NAME}...")
        model = TextEmbedding(model_name=MODEL_NAME)

        _generate_set_embeddings(conn, model)
        _generate_part_embeddings(conn, model)

    finally:
        if standalone:
            conn.close()
            print("Génération des embeddings terminée.")


def _generate_set_embeddings(conn, model):
    """Encode chaque set avec son nom + nom du thème."""
    print("\nGénération des embeddings pour les sets...")

    # JOIN avec themes pour enrichir le texte encodé
    rows = conn.execute("""
        SELECT s.set_num,
               s.name || COALESCE(' ' || t.name, '') AS text
        FROM sets s
        LEFT JOIN themes t ON s.theme_id = t.id
    """).fetchall()
    print(f"  {len(rows)} sets à encoder")

    conn.execute("DELETE FROM set_embeddings")

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i : i + BATCH_SIZE]
        set_nums = [r[0] for r in batch]
        texts = [r[1] for r in batch]
        embeddings = list(model.embed(texts))
        conn.executemany(
            "INSERT INTO set_embeddings VALUES (?, ?)",
            [(set_nums[j], embeddings[j].tolist()) for j in range(len(batch))],
        )
        print(f"  Sets : {min(i + BATCH_SIZE, len(rows))}/{len(rows)}")

    print("  Création de l'index HNSW pour set_embeddings...")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS hnsw_sets ON set_embeddings USING HNSW(embedding)"
    )


def _generate_part_embeddings(conn, model):
    """Encode chaque pièce avec son nom + nom de la catégorie."""
    print("\nGénération des embeddings pour les pièces...")

    # JOIN avec part_categories pour enrichir le texte encodé
    rows = conn.execute("""
        SELECT p.part_num,
               p.name || COALESCE(' ' || pc.name, '') AS text
        FROM parts p
        LEFT JOIN part_categories pc ON p.part_cat_id = pc.id
    """).fetchall()
    print(f"  {len(rows)} pièces à encoder")

    conn.execute("DELETE FROM part_embeddings")

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i : i + BATCH_SIZE]
        part_nums = [r[0] for r in batch]
        texts = [r[1] for r in batch]
        embeddings = list(model.embed(texts))
        conn.executemany(
            "INSERT INTO part_embeddings VALUES (?, ?)",
            [(part_nums[j], embeddings[j].tolist()) for j in range(len(batch))],
        )
        print(f"  Pièces : {min(i + BATCH_SIZE, len(rows))}/{len(rows)}")

    print("  Création de l'index HNSW pour part_embeddings...")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS hnsw_parts ON part_embeddings USING HNSW(embedding)"
    )


if __name__ == "__main__":
    generate_embeddings()
