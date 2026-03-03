import pytest


@pytest.fixture(autouse=True)
def pg_rollback():
    """Override du fixture pg_rollback pour les tests de service (pas de BDD nécessaire)."""
    yield
