from typing import Optional

from pydantic import BaseModel


class {{ __template_plural_namespace_caps }}QueryParams(BaseModel):
    {% for field in __template_fields %}
    {{ field[0] }}: Optional[{{ field[1] }}] = None{% endfor %}


class {{ __template_plural_namespace_caps }}Base(BaseModel):
    {% for field in __template_fields %}
    {{ field[0] }}: {{ field[1] }}{% endfor %}


class {{ __template_plural_namespace_caps }}Create({{ __template_plural_namespace_caps }}Base):
    ...


class {{ __template_plural_namespace_caps }}Update({{ __template_plural_namespace_caps }}Base):
    ...
