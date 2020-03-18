from typing import Dict

STATUS = int

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
        "correctProductData": 8
    },
    "request": {
        "badArguments": 9
    }
}
