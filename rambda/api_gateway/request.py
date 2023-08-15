import os

from dataclasses import dataclass


@dataclass
class Request:
    jwt_claims: dict | None
    raw_event: dict | None
    headers: dict

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
