import os
from pathlib import Path

from dotenv import load_dotenv
import duckdb


load_dotenv()

# Configuration
_DB_DIR = Path(__file__).resolve().parent
DB_FILE = str(_DB_DIR / "lego.duckdb")
TEST_DB_FILE = str(_DB_DIR / "lego_test.duckdb")

# URLs des fichiers CSV (gzip)
URLS = {
    "themes": os.getenv("URL_BDD_THEMES"),
    "colors": os.getenv("URL_BDD_COLORS"),
    "part_categories": os.getenv("URL_BDD_PART_CATEGORIES"),
    "parts": os.getenv("URL_BDD_PARTS"),
    "part_relationships": os.getenv("URL_BDD_PART_RELATIONSHIPS"),
    "elements": os.getenv("URL_BDD_ELEMENTS"),
    "sets": os.getenv("URL_BDD_SETS"),
    "minifigs": os.getenv("URL_BDD_MINIFIGS"),
    "inventories": os.getenv("URL_BDD_INVENTORIES"),
    "inventory_parts": os.getenv("URL_BDD_INVENTORY_PARTS"),
    "inventory_sets": os.getenv("URL_BDD_INVENTORY_SETS"),
    "inventory_minifigs": os.getenv("URL_BDD_INVENTORY_MINIFIGS"),
}


def create_schema(conn):
    """Crée le schéma de la base de données depuis le fichier SQL"""
    print(" Création du schéma...")

    # Lire le fichier SQL
    base_dir = Path(__file__).resolve().parent
    schema_path = base_dir / "schema_lego.sql"
    if not schema_path.exists():
        print("❌ Fichier schema_lego.sql introuvable")
        return False

    with open(schema_path) as f:
        sql_commands = f.read()

    # Exécuter le schéma
    try:
        conn.execute(sql_commands)
        print("✅ Schéma créé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du schéma: {e}")
        return False


def read_rebrickable_csv(url):
    return f"""
        FROM read_csv_auto(
        '{url}',
        compression='gzip')
"""


def load_data(conn):
    """Charge les données depuis les URLs"""
    print("\n📥 Chargement des données depuis les URLs...")

    tables_order = [
        "themes",
        "colors",
        "part_categories",
        "parts",
        "part_relationships",
        "elements",
        "sets",
        "minifigs",
        "inventories",
        "inventory_parts",
        "inventory_sets",
        "inventory_minifigs",
    ]

    for table in tables_order:
        if table not in URLS or not URLS[table]:
            print(f"⚠️  URL manquante pour {table}")
            continue

        try:
            print(f"  {table:20} ...", end=" ")

            # Mapping explicite des colonnes pour chaque table
            if table == "themes":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT id, name, parent_id
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "colors":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT id, name, rgb, is_trans
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "part_categories":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT id, name
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "parts":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT part_num, name, part_cat_id
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "part_relationships":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT rel_type, child_part_num, parent_part_num
                    FROM (
                        {read_rebrickable_csv(URLS[table])}
                    ) pr
                    WHERE EXISTS (SELECT 1 FROM parts WHERE part_num = pr.child_part_num)
                      AND EXISTS (SELECT 1 FROM parts WHERE part_num = pr.parent_part_num)
                """)
            elif table == "elements":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT element_id, part_num, color_id
                    FROM (
                        {read_rebrickable_csv(URLS[table])}
                    ) e
                    WHERE EXISTS (SELECT 1 FROM parts WHERE part_num = e.part_num)
                      AND EXISTS (SELECT 1 FROM colors WHERE id = e.color_id)
                """)
            elif table == "sets":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT set_num, name, year, theme_id, num_parts, img_url
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "minifigs":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT fig_num, name, num_parts
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "inventories":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT id, version, set_num
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "inventory_parts":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT inventory_id, part_num, color_id, quantity, is_spare
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "inventory_sets":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT inventory_id, set_num, quantity
                    {read_rebrickable_csv(URLS[table])}
                """)
            elif table == "inventory_minifigs":
                conn.execute(f"""
                    INSERT INTO {table}
                    SELECT inventory_id, fig_num, quantity
                    {read_rebrickable_csv(URLS[table])}
                """)

            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"✅ {count:,} lignes")

        except Exception as e:
            print(f"❌ Erreur: {e}")


def load_test_data(conn):
    """Charge un sous-ensemble cohérent pour la base de test.

    Ordre de chargement pensé pour respecter les FK actives :
      1. Tables de référence (themes, colors, part_categories) — toutes les lignes
      2. sets (LIMIT 100) → inventories → inventory_parts (FK commentées → OK)
      3. parts dérivés des inventory_parts → part_relationships, elements
      4. minifigs, inventory_sets, inventory_minifigs
    """
    print("\n📥 Chargement du sous-ensemble de test...")

    def csv(key):
        return read_rebrickable_csv(URLS[key])

    def _check(key):
        if not URLS.get(key):
            print(f"  ⚠️  URL manquante pour {key}")
            return False
        return True

    def _count(table):
        return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    # ── 1. Tables de référence (complètes, petites) ─────────────────────────

    for table, query in [
        ("themes", "SELECT id, name, parent_id"),
        ("colors", "SELECT id, name, rgb, is_trans"),
        ("part_categories", "SELECT id, name"),
    ]:
        if not _check(table):
            continue
        print(f"  {table:20} ...", end=" ")
        try:
            conn.execute(f"INSERT INTO {table} {query} {csv(table)}")
            print(f"✅ {_count(table):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    # ── 2. Sets (100 premiers) ───────────────────────────────────────────────

    if _check("sets"):
        print(f"  {'sets':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO sets
                SELECT set_num, name, year, theme_id, num_parts, img_url
                FROM ({csv("sets")}) LIMIT 100
            """)
            print(f"✅ {_count('sets'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    # ── 3. Inventaires des sets chargés ─────────────────────────────────────

    if _check("inventories"):
        print(f"  {'inventories':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO inventories
                SELECT id, version, set_num
                FROM ({csv("inventories")}) inv
                WHERE inv.set_num IN (SELECT set_num FROM sets)
            """)
            print(f"✅ {_count('inventories'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    # ── 4. Pièces d'inventaire (FK commentées → on peut charger librement) ──

    if _check("inventory_parts"):
        print(f"  {'inventory_parts':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO inventory_parts
                SELECT inventory_id, part_num, color_id, quantity, is_spare
                FROM ({csv("inventory_parts")}) ip
                WHERE ip.inventory_id IN (SELECT id FROM inventories)
            """)
            print(f"✅ {_count('inventory_parts'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    # ── 5. Parts dérivées des inventory_parts (FK active → doit exister) ────

    if _check("parts"):
        print(f"  {'parts':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO parts
                SELECT part_num, name, part_cat_id
                FROM ({csv("parts")}) p
                WHERE p.part_num IN (
                    SELECT DISTINCT part_num FROM inventory_parts
                )
            """)
            print(f"✅ {_count('parts'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    # ── 6. Relations et éléments (filtrés sur les parts chargées) ────────────

    if _check("part_relationships"):
        print(f"  {'part_relationships':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO part_relationships
                SELECT rel_type, child_part_num, parent_part_num
                FROM ({csv("part_relationships")}) pr
                WHERE pr.child_part_num IN (SELECT part_num FROM parts)
                  AND pr.parent_part_num IN (SELECT part_num FROM parts)
            """)
            print(f"✅ {_count('part_relationships'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    if _check("elements"):
        print(f"  {'elements':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO elements
                SELECT element_id, part_num, color_id
                FROM ({csv("elements")}) e
                WHERE e.part_num IN (SELECT part_num FROM parts)
                  AND e.color_id IN (SELECT id FROM colors)
            """)
            print(f"✅ {_count('elements'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    # ── 7. Tables d'inventaire restantes ─────────────────────────────────────

    if _check("inventory_sets"):
        print(f"  {'inventory_sets':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO inventory_sets
                SELECT inventory_id, set_num, quantity
                FROM ({csv("inventory_sets")}) iset
                WHERE iset.inventory_id IN (SELECT id FROM inventories)
            """)
            print(f"✅ {_count('inventory_sets'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    if _check("minifigs"):
        print(f"  {'minifigs':20} ...", end=" ")
        try:
            conn.execute(
                f"INSERT INTO minifigs SELECT fig_num, name, num_parts FROM ({csv('minifigs')}) LIMIT 50"
            )
            print(f"✅ {_count('minifigs'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")

    if _check("inventory_minifigs"):
        print(f"  {'inventory_minifigs':20} ...", end=" ")
        try:
            conn.execute(f"""
                INSERT INTO inventory_minifigs
                SELECT inventory_id, fig_num, quantity
                FROM ({csv("inventory_minifigs")}) im
                WHERE im.inventory_id IN (SELECT id FROM inventories)
            """)
            print(f"✅ {_count('inventory_minifigs'):,} lignes")
        except Exception as e:
            print(f"❌ {e}")


def generate_embeddings_if_available(conn):
    """Génère les embeddings si fastembed est installé.

    Appelé à la fin de l'init — silencieusement ignoré si la dépendance manque.
    """
    try:
        from app.database.duckdb.generate_embeddings import generate_embeddings

        print("\n📐 Génération des embeddings (fastembed détecté)...")
        generate_embeddings(conn)
    except ImportError:
        print(
            "\n⚠️  fastembed non installé — embeddings ignorés.\n"
            "   Pour les activer : uv add fastembed\n"
            "   puis relancer : python app/database/duckdb/generate_embeddings.py"
        )


def main(db_file, test_mode: bool = False):
    """Initialise une base DuckDB.

    Args:
        db_file: Chemin du fichier .duckdb à créer.
        test_mode: Si True, charge seulement un sous-ensemble de données
                   (100 sets, parts dérivées) pour des tests rapides.
    """
    label = "TEST" if test_mode else "PRODUCTION"
    print(f"INITIALISATION DE LA BASE DE DONNÉES LEGO [{label}]")
    print(f"\nConnexion à DuckDB ({db_file})...")

    conn = duckdb.connect(db_file)

    print("Installation de l'extension httpfs...")
    conn.execute("INSTALL httpfs; LOAD httpfs")

    if not create_schema(conn):
        conn.close()
        return

    if test_mode:
        load_test_data(conn)
    else:
        load_data(conn)

    generate_embeddings_if_available(conn)

    conn.close()

    print("✅ INITIALISATION TERMINÉE")
    print(f"Fichier créé: {db_file}")


if __name__ == "__main__":
    if not Path(DB_FILE).exists():
        print(f"📦 Création de {DB_FILE}")
        main(DB_FILE, test_mode=False)

    if not Path(TEST_DB_FILE).exists():
        print(f"🧪 Création de {TEST_DB_FILE} (sous-ensemble de test)")
        main(TEST_DB_FILE, test_mode=True)
