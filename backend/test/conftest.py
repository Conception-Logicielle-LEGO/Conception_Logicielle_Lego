from dotenv import load_dotenv
import pytest

from app.database.connexion import DB_TEST_PATH, get_connection
from app.database.dao.user_dao import UserDAO


load_dotenv()


@pytest.fixture(scope="session")
def init_test_db():
    """
    Initialise la base de données de test une seule fois par session
    """
    # Supprimer l'ancienne base de test si elle existe
    if DB_TEST_PATH.exists():
        DB_TEST_PATH.unlink()

    # Initialiser la base de test
    from app.database.duckdb import init_db

    test_db_file = "lego_test.duckdb"
    init_db.main(test_db_file)

    yield

    # Optionnel : nettoyer après tous les tests
    # if DB_TEST_PATH.exists():
    #     DB_TEST_PATH.unlink()


@pytest.fixture(scope="function")
def db_connection_test():  # init_test_db en paramètre ?
    """
    Fournit une connexion DuckDB pour chaque test
    La connexion est automatiquement fermée après le test
    """
    conn = get_connection(read_only=False, test=True)
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def clean_user_tables(db_connection_test):
    """
    Nettoie uniquement les tables utilisateur avant chaque test
    Laisse les données Rebrickable intactes
    """
    user_tables = ["user_parts", "user_owned_sets", "favorite_sets", "users"]

    for table in user_tables:
        try:
            db_connection_test.execute(f"DELETE FROM {table}")
        except Exception as e:
            print(f"Erreur lors du nettoyage de {table}: {e}")
            raise

    # Réinitialiser la séquence des IDs utilisateurs
    try:
        db_connection_test.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1")
    except Exception as e:
        print(f"Erreur lors de la réinitialisation de la séquence: {e}")

    yield db_connection_test


@pytest.fixture(scope="function")
def clean_all_tables(db_connection_test):
    """
    Nettoie TOUTES les tables (y compris Rebrickable)
    À utiliser seulement si nécessaire car c'est plus lent
    """
    # Ordre inverse pour respecter les contraintes de clés étrangères
    all_tables = [
        "user_parts",
        "user_owned_sets",
        "favorite_sets",
        "users",
        "inventory_minifigs",
        "inventory_sets",
        "inventory_parts",
        "inventories",
        "minifigs",
        "sets",
        "elements",
        "part_relationships",
        "parts",
        "part_categories",
        "colors",
        "themes",
    ]

    for table in all_tables:
        try:
            db_connection_test.execute(f"DELETE FROM {table}")
        except Exception as e:
            print(f"Erreur lors du nettoyage de {table}: {e}")
            raise

    yield db_connection_test


@pytest.fixture
def user_dao(db_connection_test):
    return UserDAO(db_connection_test)
