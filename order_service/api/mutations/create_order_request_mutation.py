from typing import Annotated

from order_service.api.schemas.order_item_schema import OrderItemSchema
from utilities.entities.base import EntityBase


class CreateOrderRequestMutation(EntityBase):
    order: Annotated[OrderItemSchema, "order list with constraints"]
