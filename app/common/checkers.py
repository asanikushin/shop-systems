from app.constants.statuses import STATUS, statuses
from typing import Dict


def check_model_options(operation: str, options: Dict, model=None) -> STATUS:
    if operation == "create":
        if "name" in options and "category" in options:
            return statuses["internal"]["correctProductData"]
        else:
            return statuses["product"]["missingData"]
    elif operation.lower() in ["patch", "put"]:
        opt_id = options.get("id", None)
        if opt_id is None or model is None:
            correct_id = True
        else:
            correct_id = (opt_id == model.id)

        if not correct_id:
            return statuses["product"]["replacingID"]
        if operation.lower() == "patch":
            requirements = ("name" in options or "category" in options)
        else:  # operation.lower() == "put"
            requirements = ("name" in options and "category" in options)

        if requirements:
            return statuses["internal"]["correctProductData"]
        else:
            return statuses["product"]["missingData"]
    else:
        raise NotImplemented()
