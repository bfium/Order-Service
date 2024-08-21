from pydantic import field_validator, conint


def validate_field(*args, **kwargs):
    return field_validator(*args, **kwargs)


def con_init(*args, **kwargs):
    return conint(*args, **kwargs)
