import pytest


@pytest.fixture(autouse=True)
def pg_rollback():
    """Override du fixture pg_rollback : les tests BO n'ont pas besoin de BDD."""
    yield
