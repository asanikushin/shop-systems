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
}
