from invoke import task
from invoke.context import Context


@task
def docs_build(ctx: Context) -> None:
    """docs_build

    Build the docs.
    """
    ctx.run(
        "mkdocs build",
        pty=True,
        echo=True,
    )
    ctx.run(
        "cp ./docs/index.md ./README.md",
        pty=True,
        echo=True,
    )
    ctx.run(
        "git add ./docs README.md",
        pty=True,
        echo=True,
    )
    ctx.run(
        "git commit -S -m '📚 Updated docs.'",
        pty=True,
        echo=True,
    )


@task
def docs_serve(ctx: Context) -> None:
    """docs_serve

    Serve the docs.
    """
    ctx.run(
        "mkdocs serve --dev-addr 127.0.0.1:8008",
        pty=True,
        echo=True,
    )
