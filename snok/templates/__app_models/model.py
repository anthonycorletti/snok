from {{ __template_name }}.kit.db import RecordModel

class {{ __template_plural_namespace_caps }}(RecordModel, table=True):
    __tablename__ = "{{ __template_plural_namespace }}"
    {% for field in __template_fields %}
    {{ field[0] }}: {{ field[1] }}{% endfor %}
