from json import JSONEncoder

import weakref


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        while type(o) == weakref.ReferenceType:
            o = o()
        try:
            return o.get_dict()
        except AttributeError:
            pass
        return o.__dict__
