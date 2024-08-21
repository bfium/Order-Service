from typing import Any
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer, ForeignKey

from utilities.data_generators.uuid_generator import generate
from utilities.data_mappers.database_wrappers.order_base_model import OrderModelBase


class OrderItemModel(OrderModelBase):
    __tablename__ = "order_item"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    def dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }

    def __repr__(self) -> str:
        return f"OrderItemModel(id={self.id!r}, order_id={self.order_id!r}, product={self.product!r}, size={self.size!r}, quantity={self.quantity!r})"
