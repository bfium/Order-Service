from datetime import datetime
from uuid import UUID

from order_service.api.entities.status import Status
from utilities.entities.base import EntityBase


class OrderResponseSchema(EntityBase):
    id: UUID
    created: datetime
    status: Status
