import datetime
import typing


def parse_timedelta(delta: typing.Optional[str]) -> typing.Optional[datetime.timedelta]:
    if delta is None:
        return None
    options = dict()
    for token in delta.split():
        unit = token[-1]
        value = int(token[:-1])
        if unit == "S":
            options["seconds"] = value
        elif unit == "M":
            options["minutes"] = value
        elif unit == "H":
            options["hours"] = value
        elif unit == "W":
            options["weeks"] = value
        else:
            raise ValueError("No such delta period")
    return datetime.timedelta(**options)
