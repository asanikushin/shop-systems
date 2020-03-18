from utils.numerator import Numerator

from typing import Dict

STATUS = int

_nums = Numerator(1)
statuses: Dict[str, Dict[str, STATUS]] = {
    "product": {
        "created": next(_nums),  # 1
        "modified": next(_nums),  # 2
        "deleted": next(_nums),  # 3
        "notExists": next(_nums),  # 4
        "returned": next(_nums),  # 5
        "missingData": next(_nums),  # 6
        "replacingID": next(_nums),  # 7
    },
    "internal": {
        "correctProductData": next(_nums),  # 8
    },
    "request": {
        "badArguments": next(_nums),  # 9
    },
    "user": {
        "created": next(_nums),  # 10
        "emailUsed": next(_nums),  # 11
        "wrongPassword": next(_nums),  # 12
        "noUser": next(_nums),  # 13
    },
    "tokens": {
        "created": next(_nums),  # 14
        "noSuchToken": next(_nums),  # 15
        "refreshExpired": next(_nums),  # 16
        "accessExpired": next(_nums),  # 17
        "accessOk": next(_nums),  # 18
    }
}
