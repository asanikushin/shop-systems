from .storage import BaseStorage
from .types import *

from app.common import Numerator
from app.common import check_model_options
from app.constants.statuses import statuses
from app.models.memory.productmodel import ProductModel


class MemoryStorage(BaseStorage):
    def __init__(self):
        self._nums = Numerator()
        self._storage = dict()
        self._data: typing.List[ProductModel] = []

    def add_product(self, name, **options) -> ID_WITH_STATUS:
        new_id = str(self._nums.next())
        options.update({"id": new_id, "name": name})
        correct = check_model_options("create", options)
        if correct != statuses["internal"]["correctProductData"]:
            return None, correct

        product = ProductModel(**options)

        self._data.append(product)
        self._storage[new_id] = len(self._data) - 1
        return new_id, statuses["product"]["created"]

    def check_product(self, prod_id) -> bool:
        return self._check_and_index(prod_id)[0]

    def get_product(self, prod_id) -> MODEL_WITH_STATUS:
        contain, index = self._check_and_index(prod_id)
        if contain:
            return self._get_index(index), statuses["product"]["returned"]
        else:
            return None, statuses["product"]["notExists"]

    def get_products(self, offset=0, count=None) -> MODELS_WITH_STATUS:
        if count is None:
            end = None
        else:
            end = offset + count
        return self._data[offset:end], statuses["product"]["returned"]

    def get_products_count(self) -> int:
        return len(self._data)

    def delete_product(self, prod_id: ID_TYPE) -> MODEL_WITH_STATUS:
        contain, index = self._check_and_index(prod_id)
        if not contain:
            return None, statuses["product"]["notExists"]
        product = self._data.pop(index)
        return product, statuses["product"]["deleted"]

    def update_product(self, prod_id, method="PATCH", **options) -> MODEL_WITH_STATUS:
        contain, index = self._check_and_index(prod_id)
        if not contain:
            return None, statuses["product"]["notExists"]
        product = self._get_index(index)

        correct = check_model_options(method, options, model=product)
        if correct != statuses["internal"]["correctProductData"]:
            return None, correct
        return product.update(**options), statuses["product"]["modified"]

    def _check_and_index(self, prod_id):
        index = self._storage.get(prod_id, None)
        return index is not None, index

    def _get_index(self, index) -> MODEL_TYPE:
        return self._data[index]
