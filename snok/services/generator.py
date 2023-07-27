import os
from typing import Any, List

from jinja2 import Template

from snok.utils import _get_project_name, _get_snok_path


class _BaseContentGenerator:
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Subclasses must implement this method.")

    def _pluralize_name(self, name: str) -> str:
        if name.endswith(("s", "x", "z", "ch", "sh")):
            return name + "es"
        elif name.endswith("y"):
            if name[-2] in ("a", "e", "i", "o", "u"):
                return name + "s"
            else:
                return name[:-1] + "ies"
        else:
            return name + "s"


class _ModelContentGenerator(_BaseContentGenerator):
    MISSING_INPUT_ERROR = (
        "Missing input. Please provide a model name and fields."
        " For example: snok generate model user name:str email:str"
    )
    BASE_FIELD_TYPES = ["str", "int", "float", "bool", "datetime"]

    def _validate_field_types(self, fields: Any) -> None:
        field_set = set(fields)
        try:
            field_types_set = set([field.split(":")[1].lower() for field in field_set])
        except IndexError:
            raise ValueError(
                "Invalid field format. Please provide a field name and type."
                " For example: snok generate model user name:str email:str"
            )
        if not field_types_set.issubset(self.BASE_FIELD_TYPES):
            invalid_field_types = field_types_set - set(self.BASE_FIELD_TYPES)
            raise ValueError(
                f"Invalid field types: {','.join(invalid_field_types)}"
                f" Please provide a valid field type, "
                f"such as {','.join(self.BASE_FIELD_TYPES)}."
            )

    def generate(self, *args: Any, **kwargs: Any) -> Any:
        _input = kwargs.get("_input")
        assert _input is not None, self.MISSING_INPUT_ERROR
        namespace, fields = _input[0].lower(), _input[1:]
        _plural_namespace = self._pluralize_name(namespace)
        self._validate_field_types(fields)
        _fields = [field.split(":") for field in fields]
        self._write_model_to_models(
            namespace=namespace, plural_namespace=_plural_namespace, fields=_fields
        )
        self._update_models_init_file(plural_namespace=_plural_namespace)

    def _write_model_to_models(
        self, namespace: str, plural_namespace: str, fields: List[List[str]]
    ) -> None:
        models_dir = f"{_get_project_name()}/models"
        model_filename = f"{models_dir}/{plural_namespace}.py"
        model_template_file = _get_snok_path() + "/templates/__app_models/model.py"
        content = Template(open(model_template_file).read()).render(
            __template_name=_get_project_name(),
            __template_namespace=namespace,
            __template_plural_namespace=plural_namespace,
            __template_plural_namespace_caps=plural_namespace.capitalize(),
            __template_fields=fields,
        )
        with open(model_filename, "w") as f:
            f.write(content)

    def _update_models_init_file(self, plural_namespace: str) -> None:
        models_dir = f"{_get_project_name()}/models"
        init_filename = f"{models_dir}/__init__.py"
        import_statement = (
            f"from {_get_project_name()}.models.{plural_namespace}"
            f" import {plural_namespace.capitalize()}\n"
        )
        with open(init_filename, "r") as f:
            lines = f.readlines()
        with open(init_filename, "w") as f:
            for line in lines:
                if line.startswith("__all__"):
                    f.write(line.replace("__all__", f"{import_statement}\n__all__"))
                elif line.startswith("]"):
                    f.write(line.replace("]", f'"{plural_namespace.capitalize()}",\n]'))
                else:
                    f.write(line)


class _RouterContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        _input = kwargs.get("_input")
        assert _input is not None, (
            "Missing input. Please provide a router name and routes."
            " For example: snok generate router myrouter route1 route2 route3"
        )
        namespace, routes = _input[0].lower(), _input[1:]
        os.makedirs(f"{_get_project_name()}/{namespace}", exist_ok=True)
        with open(f"{_get_project_name()}/{namespace}/__init__.py", "w") as f:
            pass
        router_filename = f"{_get_project_name()}/{namespace}/router.py"
        router_template_file = _get_snok_path() + "/templates/__app_router/router.py"
        content = Template(open(router_template_file).read()).render(
            __template_name=_get_project_name(),
            __template_router_name=namespace,
            __template_router_routes=routes,
        )
        with open(router_filename, "w") as router_py:
            router_py.write(content)

        # update routers.py with import statement
        routers_file = f"{_get_project_name()}/router.py"
        import_statement = (
            f"from {_get_project_name()}.{namespace}.router"
            f" import router as {namespace}_router\n"
        )
        with open(routers_file, "r") as f:
            lines = f.readlines()
        with open(routers_file, "w") as f:
            for line in lines:
                if line.startswith("router = APIRouter(\n"):
                    f.write(
                        line.replace(
                            "router = APIRouter(\n",
                            f"{import_statement}\n\nrouter = APIRouter(\n",
                        )
                    )
                else:
                    f.write(line)
            f.write(f"\nrouter.include_router(router={namespace}_router)\n")


class _ScaffoldContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        _input = kwargs.get("_input")
        assert _input is not None, (
            "Missing input. Please provide a model name and fields."
            " For example: snok generate scaffold person name:str age:int"
        )
        mcg = _ModelContentGenerator()
        mcg.generate(*args, **kwargs)

        namespace, fields = _input[0].lower(), _input[1:]
        _fields = [field.split(":") for field in fields]
        _plural_namespace = self._pluralize_name(namespace)
        os.makedirs(f"{_get_project_name()}/{_plural_namespace}", exist_ok=True)
        with open(f"{_get_project_name()}/{_plural_namespace}/__init__.py", "w") as f:
            pass
        os.makedirs(
            f"{_get_project_name()}/../tests/{_plural_namespace}", exist_ok=True
        )
        with open(
            f"{_get_project_name()}/../tests/{_plural_namespace}/__init__.py", "w"
        ) as f:
            pass

        # generate scaffolded router
        scaffolded_router_filename_dst = (
            f"{_get_project_name()}/{_plural_namespace}/router.py"
        )
        scaffolded_router_filename_src = (
            f"{_get_snok_path()}/templates/__app_scaffold/router.py"
        )
        content = Template(open(scaffolded_router_filename_src).read()).render(
            __template_name=_get_project_name(),
            __template_plural_namespace=_plural_namespace,
            __template_plural_namespace_caps=_plural_namespace.capitalize(),
            __template_namespace=namespace,
        )
        with open(scaffolded_router_filename_dst, "w") as f:
            f.write(content)

        # generate scaffolded service
        scaffolded_service_filename_dst = (
            f"{_get_project_name()}/{_plural_namespace}/service.py"
        )
        scaffolded_service_filename_src = (
            f"{_get_snok_path()}/templates/__app_scaffold/service.py"
        )
        content = Template(open(scaffolded_service_filename_src).read()).render(
            __template_name=_get_project_name(),
            __template_plural_namespace=_plural_namespace,
            __template_plural_namespace_caps=_plural_namespace.capitalize(),
            __template_namespace=namespace,
        )
        with open(scaffolded_service_filename_dst, "w") as f:
            f.write(content)

        # generate scaffolded schemas
        scaffolded_schemas_filename_dst = (
            f"{_get_project_name()}/{_plural_namespace}/schemas.py"
        )
        scaffolded_schemas_filename_src = (
            f"{_get_snok_path()}/templates/__app_scaffold/schemas.py"
        )
        content = Template(open(scaffolded_schemas_filename_src).read()).render(
            __template_name=_get_project_name(),
            __template_plural_namespace=_plural_namespace,
            __template_plural_namespace_caps=_plural_namespace.capitalize(),
            __template_namespace=namespace,
            __template_fields=_fields,
        )
        with open(scaffolded_schemas_filename_dst, "w") as f:
            f.write(content)

        # generate scaffolded tests

        scaffolded_tests_filename_dst = (
            f"{_get_project_name()}/../tests/{_plural_namespace}/test_router.py"
        )
        scaffolded_tests_filename_src = (
            f"{_get_snok_path()}/templates/__app_scaffold_tests/test_router.py"
        )
        content = Template(open(scaffolded_tests_filename_src).read()).render(
            __template_name=_get_project_name(),
            __template_plural_namespace=_plural_namespace,
            __template_plural_namespace_caps=_plural_namespace.capitalize(),
            __template_namespace=namespace,
        )
        with open(scaffolded_tests_filename_dst, "w") as f:
            f.write(content)

        # update routers.py with import statement
        routers_file = f"{_get_project_name()}/router.py"
        import_statement = (
            f"from {_get_project_name()}.{_plural_namespace}.router"
            f" import router as {_plural_namespace}_router\n"
        )
        with open(routers_file, "r") as f:
            lines = f.readlines()
        with open(routers_file, "w") as f:
            for line in lines:
                if line.startswith("router = APIRouter(\n"):
                    f.write(
                        line.replace(
                            "router = APIRouter(\n",
                            f"{import_statement}\n\nrouter = APIRouter(\n",
                        )
                    )
                else:
                    f.write(line)
            f.write(f"\nrouter.include_router(router={_plural_namespace}_router)\n")
