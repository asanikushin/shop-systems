from app import constants
from app.storage import DBStorage

from app.common.errorResponse import create_error_with_status

from flask import jsonify, request


def get_products():
    options = dict()
    if "offset" in request.args:
        options["offset"] = request.args.get("offset", type=int)
    if "count" in request.args:
        options["count"] = request.args.get("count", type=int)

    if "offset" in options and options["offset"] < 0:
        return jsonify(
            create_error_with_status(constants.statuses["request"]["badArguments"], "Offset cann't be negative")), \
               constants.common_responses["Bad request"]

    products, status = DBStorage.get_products(**options)
    http_status = constants.responses[status]
    total_count = DBStorage.get_products_count()
    if len(options) != 0:
        options["count"] = len(products)
        options["offset"] = options.get("offset", 0)
    return jsonify(products=products, total_count=total_count, status=status, **options), http_status


def get_product(prod_id=None):
    prod_id = prod_id or request.args.get("id")
    product, status = DBStorage.get_product(prod_id)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["returned"]:
        body = dict(product=product, status=status)
    else:
        body = create_error_with_status(status, "no such product id: {{ID}}", ID=prod_id)
    return jsonify(body), http_status
