from {{ __template_name }}.main import foo


def test_foo() -> None:
    assert foo() == "bar"
