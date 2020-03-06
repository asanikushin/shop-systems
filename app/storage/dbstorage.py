from .storage import BaseStorage
from .types import *

from app.common import check_model_options
from app.constants.statuses import statuses

from app.models.database.product import Product

from app import db


class SQLStorage(BaseStorage):
    def __init__(self):
        self._db = db

    def add_product(self, name, **options) -> ID_WITH_STATUS:
        options.update({"name": name})
        correct = check_model_options("create", options)
        if correct != statuses["internal"]["correctProductData"]:
            return None, correct

        product = Product(**options)
        self._db.session.add(product)
        self._db.session.commit()
        return product.id, statuses["product"]["created"]

    def check_product(self, prod_id) -> bool:
        return Product.query.get(prod_id) is not None

    def get_product(self, prod_id) -> MODEL_WITH_STATUS:
        product = self._get_product(prod_id)
        if product is not None:
            return product, statuses["product"]["returned"]
        else:
            return None, statuses["product"]["notExists"]

    def get_products(self, offset=0, count=None) -> MODELS_WITH_STATUS:
        query = self._db.session.query(Product).offset(offset)
        if count is not None:
            query = query.limit(count)
        return query.all(), statuses["product"]["returned"]

    def get_products_count(self) -> int:
        return self._db.session.query(Product).count()

    def delete_product(self, prod_id: ID_TYPE) -> MODEL_WITH_STATUS:
        product = self._get_product(prod_id)
        if product is None:
            return None, statuses["product"]["notExists"]
        self._db.session.delete(product)
        return product, statuses["product"]["deleted"]

    def update_product(self, prod_id, method="PATCH", **options) -> MODEL_WITH_STATUS:
        product = self._get_product(prod_id)
        if product is None:
            return None, statuses["product"]["notExists"]

        correct = check_model_options(method, options, model=product)
        if correct != statuses["internal"]["correctProductData"]:
            return None, correct
        return product.values_update(**options), statuses["product"]["modified"]

    @staticmethod
    def _get_product(prod_id) -> MODEL_TYPE:
        return Product.query.get(prod_id)
