from typing import Optional

from order_service.api.entities.size import Size
from utilities.entities.base import EntityBase
from utilities.data_validators.entity_validator import con_init, validate_field


class OrderItemSchema(EntityBase):
    product: str
    size: Size
    quantity: Optional[con_init(ge=1, strict=True)] = 1

    @validate_field("quantity")
    def validate_quantity(cls, v):
        assert v is not None, "quantity cannot be None"
        return v
