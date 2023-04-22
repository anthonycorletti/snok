import json
import os

os.environ["TZ"] = "UTC"


def foo() -> str:
    json.dumps({"foo0": "bar"})
    return "foo"
