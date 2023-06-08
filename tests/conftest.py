import os
import shutil
from typing import Generator

import pytest
from typer.testing import CliRunner


@pytest.fixture(scope="function")
def cli_runner() -> Generator:
    r = CliRunner()
    yield r


@pytest.fixture(scope="function", autouse=True)
def setup_test_content_output_dir() -> Generator:
    _dir = f"tmp/test_content_output_{os.getpid()}"
    os.makedirs(_dir, exist_ok=True)
    yield _dir
    shutil.rmtree(_dir)
