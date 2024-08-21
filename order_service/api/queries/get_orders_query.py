from typing import List

from order_service.api.schemas.order_response_schema import OrderResponseSchema
from utilities.entities.base import EntityBase


class GetOrdersQuery(EntityBase):
    orders: list[OrderResponseSchema]
