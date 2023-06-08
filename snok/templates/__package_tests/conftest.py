import pytest


@pytest.fixture(scope="session", autouse=True)
def _session() -> None:
    pass


@pytest.fixture(scope="module", autouse=True)
def _module() -> None:
    pass
