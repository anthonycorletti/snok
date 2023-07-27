import importlib.resources as resources
import os
import re

from jinja2 import Template

from snok.const import ProjectType


class BaseNewService:
    def __init__(self) -> None:
        import snok

        self.root_template_dir = str(resources.files(snok)) + "/templates"

    def create(
        self,
        name: str,
        desc: str,
        output_dir: str,
        type: ProjectType = ProjectType.package,
    ) -> None:
        raise NotImplementedError("create() must be implemented by subclass.")

    def _render_content_directory(
        self,
        name: str,
        desc: str,
        source_dir: str,
        output_dir: str,
        type: ProjectType = ProjectType.package,
    ) -> None:
        for root, dirs, files in os.walk(source_dir):
            if not ("__pycache__" in root or "_cache" in root):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, source_dir)
                    output_path = os.path.join(output_dir, relative_path)

                    if output_path.endswith("_pyproject_toml"):
                        output_path = output_path.replace(
                            "_pyproject_toml", "pyproject.toml"
                        )
                        if type == ProjectType.app:
                            with open(file_path, "r") as f:
                                content = f.read()
                                if "--asyncio-mode=auto" not in content:
                                    content = content.replace(
                                        '"console_output_style=progress"',
                                        '"console_output_style=progress"\n'
                                        ', "--asyncio-mode=auto"',
                                    )
                            tmp_file = file_path + ".tmp"
                            with open(tmp_file, "w") as f:
                                f.write(content)
                            self._render_content_file(
                                name=name,
                                desc=desc,
                                source_path=tmp_file,
                                output_path=output_path,
                            )
                            os.remove(tmp_file)
                            continue

                    if output_path.endswith("alembic.ini"):
                        output_path = output_path.replace(
                            "migrations/alembic.ini", "alembic.ini"
                        )

                    if output_path.endswith("py.typed"):
                        output_path = output_path.replace(
                            "py.typed", f"{name}/py.typed"
                        )

                    # TODO: Add support for htmx and tailwind
                    if output_path.endswith("tailwind.config.js"):
                        output_path = output_path.replace(  # pragma: no cover
                            "static/tailwind.config.js", "tailwind.config.js"
                        )

                    _basename = os.path.basename(relative_path)
                    if _basename.startswith("_.") and not _basename.endswith(".py"):
                        _newbasename = _basename.replace("_.", ".")
                        output_path = os.path.join(
                            output_dir,
                            relative_path.replace(_basename, _newbasename),
                        )

                    if re.match(r"^.*\.env.*$", output_path):
                        b = os.path.basename(output_path)
                        output_path = output_path.replace(f"{name}/{b}", b)

                    self._render_content_file(
                        name=name,
                        desc=desc,
                        source_path=file_path,
                        output_path=output_path,
                    )

    def _render_content_file(
        self,
        name: str,
        desc: str,
        source_path: str,
        output_path: str,
    ) -> None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if self._file_is_image_file(file_path=source_path):
            # TODO: Add support for images for rendering in frontend
            with open(source_path, "rb") as source_file:  # pragma: no cover
                with open(output_path, "wb") as output_file:
                    output_file.write(source_file.read())
        else:
            with open(source_path, "r") as source_file:
                source_content = source_file.read()
                with open(output_path, "w") as output_file:
                    output_file.write(
                        self._render_output_content_string(
                            source_path=source_path,
                            source_content=source_content,
                            name=name,
                            desc=desc,
                        )
                    )

    def _file_is_image_file(self, file_path: str) -> bool:
        return os.path.splitext(file_path)[1] in [".png", ".jpg", ".jpeg", ".gif"]

    def _render_output_content_string(
        self, source_path: str, source_content: str, name: str, desc: str
    ) -> str:
        return (
            source_content
            if os.path.splitext(source_path)[1] == ".html"
            else Template(source_content).render(
                __template_name=name,
                __template_description=desc,
            )
        )


class NewPackageService(BaseNewService):
    def __init__(self) -> None:
        super().__init__()

    def create(
        self,
        name: str,
        desc: str,
        output_dir: str,
        type: ProjectType = ProjectType.package,
    ) -> None:
        shared_template_dir = f"{self.root_template_dir}/__shared"
        package_template_dir = f"{self.root_template_dir}/__{type.value}"
        tests_template_dir = f"{self.root_template_dir}/__{type.value}_tests"
        os.makedirs(output_dir, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=shared_template_dir,
            output_dir=output_dir,
            type=type,
        )
        package_root = f"{output_dir}/{name}"
        os.makedirs(package_root, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=package_template_dir,
            output_dir=package_root,
            type=type,
        )
        package_test_root = f"{output_dir}/tests"
        os.makedirs(package_test_root, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=tests_template_dir,
            output_dir=package_test_root,
            type=type,
        )
        if not os.path.exists(f"{output_dir}/.git"):
            os.system(f"git init {output_dir} > /dev/null 2>&1")


class NewAppService(BaseNewService):
    def __init__(self) -> None:
        super().__init__()

    def create(
        self,
        name: str,
        desc: str,
        output_dir: str,
        type: ProjectType = ProjectType.app,
    ) -> None:
        shared_template_dir = f"{self.root_template_dir}/__shared"
        app_template_dir = f"{self.root_template_dir}/__{type.value}"
        app_tests_template_dir = f"{self.root_template_dir}/__{type.value}_tests"
        app_migrations_templates_dir = (
            f"{self.root_template_dir}/__{type.value}_migrations"
        )
        # TODO: frontend with htmx and tailwind
        # app_views_templates_dir = f"{self.root_template_dir}/__{type.value}_views"
        # app_static_templates_dir = f"{self.root_template_dir}/__{type.value}_static"
        os.makedirs(output_dir, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=shared_template_dir,
            output_dir=output_dir,
            type=type,
        )
        app_root = f"{output_dir}/{name}"
        os.makedirs(app_root, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=app_template_dir,
            output_dir=app_root,
            type=type,
        )
        app_test_root = f"{output_dir}/tests"
        os.makedirs(app_test_root, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=app_tests_template_dir,
            output_dir=app_test_root,
            type=type,
        )
        app_migrations_root = f"{output_dir}/migrations"
        os.makedirs(app_migrations_root, exist_ok=True)
        self._render_content_directory(
            name=name,
            desc=desc,
            source_dir=app_migrations_templates_dir,
            output_dir=app_migrations_root,
            type=type,
        )
        # TODO: frontend with htmx and tailwind
        # app_views_root = f"{output_dir}/views"
        # os.makedirs(app_views_root, exist_ok=True)
        # self._render_content_directory(
        #     name=name,
        #     desc=desc,
        #     source_dir=app_views_templates_dir,
        #     output_dir=app_views_root,
        #     type=type,
        # )
        # app_template_root = f"{output_dir}/static"
        # os.makedirs(app_template_root, exist_ok=True)
        # self._render_content_directory(
        #     name=name,
        #     desc=desc,
        #     source_dir=app_static_templates_dir,
        #     output_dir=app_template_root,
        #     type=type,
        # )
        if not os.path.exists(f"{output_dir}/.git"):
            os.system(f"git init {output_dir} > /dev/null 2>&1")
