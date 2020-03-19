from .statuses import STATUS, statuses
from typing import Dict

RESPONSE = int

responses: Dict[STATUS, RESPONSE] = {
    statuses["product"]["created"]: 201,
    statuses["product"]["modified"]: 202,
    statuses["product"]["deleted"]: 200,
    statuses["product"]["notExists"]: 404,
    statuses["product"]["returned"]: 200,
    statuses["product"]["missingData"]: 400,
    statuses["product"]["replacingID"]: 403,

    statuses["request"]["badArguments"]: 400,

    statuses["user"]["created"]: 201,
    statuses["user"]["emailUsed"]: 406,
    statuses["user"]["wrongPassword"]: 403,
    statuses["user"]["noUser"]: 404,
    statuses["user"]["missingData"]: 400,

    statuses["tokens"]["created"]: 201,
    statuses["tokens"]["noSuchToken"]: 404,
    statuses["tokens"]["refreshTokenExpired"]: 403,
    statuses["tokens"]["accessTokenExpired"]: 403,
    statuses["tokens"]["accessOk"]: 200,
    statuses["tokens"]["missingData"]: 400,
}

common_responses: Dict[str, RESPONSE] = {
    "Bad request": 400,
    "No auth": 401,
    "Not found": 404,
}
