import os
from pathlib import Path

from dotenv import load_dotenv
import duckdb


load_dotenv()

# Configuration
DB_FILE = "lego.duckdb"
TEST_DB_FILE = "lego_test.duckdb"

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
    schema_path = base_dir / "schema.sql"
    if not schema_path.exists():
        print("❌ Fichier schema.sql introuvable")
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
                    SELECT set_num, name, year, theme_id, num_parts
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


def main(db_file):
    """Initialise une base DuckDB"""

    print("INITIALISATION DE LA BASE DE DONNÉES LEGO")
    print(f"\nConnexion à DuckDB ({db_file})...")

    conn = duckdb.connect(db_file)

    print("Installation de l'extension httpfs...")
    conn.execute("INSTALL httpfs; LOAD httpfs")

    if not create_schema(conn):
        conn.close()
        return

    load_data(conn)

    conn.close()

    print("✅ INITIALISATION TERMINÉE")
    print(f"Fichier créé: {db_file}")


if __name__ == "__main__":
    if not Path(DB_FILE).exists():
        print(f"📦 Création de {DB_FILE}")
        main(DB_FILE)

    if not Path(TEST_DB_FILE).exists():
        print(f"🧪 Création de {TEST_DB_FILE}")
        main(TEST_DB_FILE)
