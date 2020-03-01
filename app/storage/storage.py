from .types import *


class BaseStorage:
    def add_product(self, name, **options) -> ID_WITH_STATUS:
        raise NotImplemented()

    def check_product(self, prod_id) -> bool:
        raise NotImplemented()

    def get_product(self, prod_id) -> MODEL_WITH_STATUS:
        raise NotImplemented()

    def get_products(self, offset=0, count=None) -> MODELS_WITH_STATUS:
        raise NotImplemented()

    def get_products_count(self) -> int:
        raise NotImplemented()

    def delete_product(self, prod_id: ID_TYPE) -> MODEL_WITH_STATUS:
        raise NotImplemented()

    def update_product(self, prod_id, **options) -> MODEL_WITH_STATUS:
        raise NotImplemented()
