import json


class ProductModel:
    def __init__(self, **options):
        self.update(**options)

    def get_dict(self):
        return self.__dict__

    def update(self, **options) -> "ProductModel":
        for key, value in options.items():
            self.__setattr__(key, value)
        return self
