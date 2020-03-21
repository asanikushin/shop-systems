from constants import STATUS
from shop.models.memory.productmodel import ProductModel as _ProductModel
from shop.models.database.product import Product as _Product

import typing

ID_TYPE = typing.Optional[int]
MODEL_TYPE = typing.Optional[typing.Union[_ProductModel, _Product]]
MODELS_TYPE = typing.List[MODEL_TYPE]

ID_WITH_STATUS = typing.Tuple[ID_TYPE, STATUS]
MODEL_WITH_STATUS = typing.Tuple[MODEL_TYPE, STATUS]
MODELS_WITH_STATUS = typing.Tuple[MODELS_TYPE, STATUS]
