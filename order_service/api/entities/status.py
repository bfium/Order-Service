from enum import Enum


# https://fastapi.tiangolo.com/fr/tutorial/path-params/#creation-dun-enum
class Status(str, Enum):
    created = 'created'
    paid = 'paid'
    cancelled = 'cancelled'
    progress = 'progress'
    canceled = 'canceled'
    dispatched = 'dispatched'
    delivered = 'delivered'
