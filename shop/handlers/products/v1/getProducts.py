import constants
from shop.storage import memoryStorage

from flask import jsonify, request


def get_products():
    options = dict()
    if "offset" in request.args:
        options["offset"] = request.args.get("offset", type=int)
    if "count" in request.args:
        options["count"] = request.args.get("count", type=int)

    products, status = memoryStorage.get_products(**options)
    http_status = constants.responses[status]
    total_count = memoryStorage.get_products_count()
    if len(options) != 0:
        options["count"] = min(max(0, total_count - options.get("offset", 0)), options.get("count", 0))
    return jsonify(products=products, total_count=total_count, status=status, **options), http_status


def get_product(prod_id=None):
    prod_id = prod_id or request.args.get("id")
    product, status = memoryStorage.get_product(prod_id)
    http_status = constants.responses[status]

    if status == constants.statuses["product"]["returned"]:
        body = jsonify(product=product, status=status)
    else:
        body = f"no such product id: {prod_id}"
    return body, http_status
