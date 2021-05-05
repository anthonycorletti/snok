import pytest


@pytest.fixture(scope="session")
def session_fixture():
    pass


@pytest.fixture(scope="module")
def module_fixture():
    pass
