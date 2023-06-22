import os


def _get_default_output_dir() -> str:
    """Returns the default output directory of the project."""
    return os.path.dirname(os.getenv("VIRTUAL_ENV", os.getcwd()))
