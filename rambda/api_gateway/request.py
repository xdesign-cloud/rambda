import json
import os
from dataclasses import dataclass
from typing import Optional

from aws_lambda_typing.events import APIGatewayProxyEventV2


@dataclass
class Request:
    headers: dict

    body: Optional[str] = None
    jwt_claims: Optional[dict] = None

    raw_event: Optional[dict] = None

    @classmethod
    def from_apigw_event(cls, event: APIGatewayProxyEventV2, include_raw_event=False):
        kwargs = {"body": event["body"], "headers": event["headers"]}

        if jwt := event["requestContext"].get("authorizer", {}).get("jwt", {}):
            kwargs["jwt_claims"] = jwt["claims"]

        if include_raw_event:
            kwargs["raw_event"] = event

        return cls(**kwargs)

    @property
    def user_id(self):
        if self.jwt_claims:
            user_id_claim = os.environ.get("RAM_JWT_USER_ID_CLAIM", "sub")
            return self.jwt_claims[user_id_claim]

        return None

    @property
    def jwt_groups(self):
        # AWS have a weird handling of the 'groups' claim, where apparently they expect
        # it to only ever be a string, so they parse it in a manner that looks like
        # [foo bar baz] - interesting because it doesn't include quotes.
        # This resulted in this hacky but simple way of parsing the groups
        return self.jwt_claims["groups"][1:-1].split()

    @property
    def json(self):
        return json.loads(self.body)
