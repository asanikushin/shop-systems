import json


def create_error_response(base, **options):
    if len(options):
        return dict(base=base, args=options)
    else:
        return dict(base=base)


def create_error_with_status(status, base, **option):
    return dict(error=create_error_response(base, **option), status=status)
