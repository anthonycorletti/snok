import importlib.resources as resources
import os

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

                    _basename = os.path.basename(relative_path)
                    if _basename.startswith("_.") and not _basename.endswith(".py"):
                        _newbasename = _basename.replace("_.", ".")
                        output_path = os.path.join(
                            output_dir,
                            relative_path.replace(_basename, _newbasename),
                        )

                    self._render_content_file(
                        name=name,
                        desc=desc,
                        source_path=file_path,
                        output_path=output_path,
                        type=type,
                    )

    def _render_content_file(
        self,
        name: str,
        desc: str,
        source_path: str,
        output_path: str,
        type: ProjectType = ProjectType.package,
    ) -> None:
        with open(source_path, "r") as source_file:
            source_content = source_file.read()
            output_content = Template(source_content).render(
                __template_name=name,
                __template_description=desc,
            )
            with open(output_path, "w") as output_file:
                output_file.write(output_content)


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
