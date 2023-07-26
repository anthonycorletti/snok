import json
from typing import Dict, List, Optional

from pydantic import BaseModel, Json, StrictInt, StrictStr, root_validator


class Scope(BaseModel):
    type: StrictStr
    http_version: StrictStr
    method: StrictStr
    scheme: StrictStr
    path: StrictStr
    headers: List
    query_string: bytes


class RequestLoggerMessage(BaseModel):
    scope: Scope
    form: Optional[Dict]
    params: Optional[Dict]
    body: Json | Dict | List | bytes | None


class ResponseLoggerMessage(BaseModel):
    status_code: StrictInt
    raw_headers: List
    body: bytes | Dict | List | None

    @root_validator(pre=True)
    def _validate_body_as_json(cls, values: Dict) -> Dict:
        _headers = values.get("raw_headers", [])
        for header in _headers:
            if header[0].decode("utf8") == "content-type":
                values["body"] = (json.loads(values["body"]) if header[1].decode("utf-8") == "application/json" else None)
        return values
