from .memstorage import MemoryStorage
from .dbstorage import SQLStorage

memoryStorage = MemoryStorage()
DBStorage = SQLStorage()

__all__ = [memoryStorage, DBStorage]
