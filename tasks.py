import sys

from invoke import task
from invoke.context import Context


def _check_pty() -> bool:
    return sys.platform not in ["win32", "cygwin", "msys"]


@task
def docs_build(ctx: Context) -> None:
    """docs_build

    Build the docs.
    """
    ctx.run(
        "mkdocs build",
        pty=_check_pty(),
        echo=True,
    )
    ctx.run(
        "cp ./docs/index.md ./README.md",
        pty=_check_pty(),
        echo=True,
    )
    ctx.run(
        "git add ./docs README.md",
        pty=_check_pty(),
        echo=True,
    )
    ctx.run(
        "git commit -S -m '📚 Updated docs.'",
        pty=_check_pty(),
        echo=True,
    )


@task
def docs_serve(ctx: Context) -> None:
    """docs_serve

    Serve the docs.
    """
    ctx.run(
        "mkdocs serve --dev-addr 127.0.0.1:8008",
        pty=_check_pty(),
        echo=True,
    )
