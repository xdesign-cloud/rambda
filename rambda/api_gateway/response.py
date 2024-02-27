import json
from dataclasses import dataclass, field

from aws_xray_sdk.core import xray_recorder


@dataclass
class Response:
    body: str
    body_as_json: bool = True
    status_code: int = 200
    headers: dict = field(default_factory=lambda: {})

    @xray_recorder.capture()
    def api_gateway_response(self):
        _headers = {"content-type": "text/plain"}

        _body = self.body
        if self.body_as_json:
            _body = json.dumps(_body)
            _headers["content-type"] = "application/json"

        _headers.update(self.headers)

        return {
            "isBase64Encoded": False,
            "statusCode": self.status_code,
            "body": _body,
            "headers": _headers,
        }
