from typing import Any

from snok.utils import _get_project_name


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
    BASE_FIELD_TYPES = ["str", "int", "float", "bool", "datetime", "date", "time"]

    def _validate_field_types(self, fields: Any) -> None:
        field_set = set(fields)
        try:
            field_types_set = set([field.split(":")[1] for field in field_set])
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
        if not _input:
            raise ValueError(self.MISSING_INPUT_ERROR)
        _model_name, fields = _input[0], _input[1:]
        _plural_model_name = self._pluralize_name(_model_name)
        self._validate_field_types(fields)
        self._write_model_to_models_py(
            model_name=_model_name, plural_model_name=_plural_model_name, fields=fields
        )

    def _write_model_to_models_py(
        self, model_name: str, plural_model_name: str, fields: Any
    ) -> None:
        models_py_filename = f"{_get_project_name()}/models.py"
        with open(models_py_filename, "a") as models_py:
            models_py.write(f"\n\nclass Base{model_name.capitalize()}(SQLModel):\n")
            for field in fields:
                field_name, field_type = field.split(":")
                models_py.write(f"    {field_name}: {field_type}\n")

            models_py.write(
                f"\n\nclass {model_name.capitalize()}("
                f"Base{model_name.capitalize()}, TimestampsMixin, UUIDMixin, table=True"
                f"):\n"
            )
            models_py.write(f"    __tablename__ = '{plural_model_name}'\n")


class _RouterContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Generating router...")
        print(args, kwargs)


class _ViewContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Generating view...")
        print(args, kwargs)


class _ScaffoldContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Scaffolding...")
        print(args, kwargs)
