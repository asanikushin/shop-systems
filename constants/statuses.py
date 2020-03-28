from utils.numerator import Numerator

from typing import Dict

STATUS = int

_nums = Numerator(1)
statuses: Dict[str, Dict[str, STATUS]] = {
    "product": {
        "created": 1,
        "modified": 2,
        "deleted": 3,
        "notExists": 4,
        "returned": 5,
        "missingData": 6,
        "replacingID": 7,
    },
    "internal": {
        "correctProductData": 8,
    },
    "request": {
        "badArguments": 9,
    },
    "user": {
        "created": 10,
        "emailUsed": 11,
        "wrongPassword": 12,
        "noUser": 13,
        "missingData": 14,
        "invalidEmail": 22,
        "notConfirmed": 23,
        "confirmed": 24,
    },
    "tokens": {
        "created": 15,
        "noSuchToken": 16,
        "refreshTokenExpired": 17,
        "accessTokenExpired": 18,
        "accessOk": 19,
        "missingData": 20,
        "invalidToken": 21,
    }
}
