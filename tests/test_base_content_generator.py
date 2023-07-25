from snok.services.generator import _BaseContentGenerator


def test_pluralize_name() -> None:
    _bcg = _BaseContentGenerator()
    assert _bcg._pluralize_name("user") == "users"
    assert _bcg._pluralize_name("users") == "userses"
    assert _bcg._pluralize_name("User") == "Users"
    assert _bcg._pluralize_name("Users") == "Userses"
    assert _bcg._pluralize_name("ax") == "axes"
    assert _bcg._pluralize_name("bogey") == "bogeys"
    assert _bcg._pluralize_name("policy") == "policies"
