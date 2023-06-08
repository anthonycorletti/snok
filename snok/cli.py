import os

from typer import Argument, Option, Typer, echo

from snok import __version__
from snok.const import APP_DESC, APP_NAME, ProjectType
from snok.services.new import NewPackageService

app = Typer(
    name=APP_NAME,
    help=APP_DESC,
    no_args_is_help=True,
)


@app.callback()
def main_callback() -> None:
    pass


main_callback.__doc__ = APP_NAME


@app.command("version")
def _version() -> None:
    """Prints the version."""
    echo(__version__, nl=False)


@app.command(
    "new",
    help="Create various types of Python projects.",
    no_args_is_help=True,
)
def _new(
    name: str = Argument(
        ...,
        help="The name of the project.",
    ),
    description: str = Option(
        "A new Python project.",
        "-d",
        "--description",
        help="The description of the project. Defaults to 'A new Python project.'",
    ),
    output_dir: str = Option(
        os.getcwd(),
        "-o",
        "--output-dir",
        help="The output directory of the project. Defaults to the current directory.",
    ),
    type: ProjectType = Option(
        "package",
        "-t",
        "--type",
        help="The type of project to create. Defaults to 'package'",
    ),
) -> None:
    new_project_service_dispatcher = {
        ProjectType.package: NewPackageService,
    }
    new_project_service = new_project_service_dispatcher[type]()
    new_project_service.create(
        name=name,
        desc=description,
        type=type,
        output_dir=output_dir,
    )
