import os
import shutil
from typing import Generator

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="function")
def cli_runner() -> Generator:
    r = CliRunner()
    yield r


@pytest.fixture(scope="function")
def setup_test_project_dir() -> Generator:
    _dir = f"tmp/test_project_{os.getpid()}"
    os.makedirs(_dir, exist_ok=True)
    yield _dir
    shutil.rmtree(_dir)
