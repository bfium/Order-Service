from typing import List, Any
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime
from datetime import datetime

from utilities.data_generators.uuid_generator import generate
from utilities.data_mappers.database_wrappers.order_base_model import OrderModelBase

from utilities.data_mappers.database_wrappers.order_item_model import OrderItemModel


class OrderModel(OrderModelBase):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate)
    user_id = Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String, default="Created", nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    schedule_id: Mapped[str] = mapped_column(String, nullable=True)
    delivery_id: Mapped[str] = mapped_column(String, nullable=True)
    items: Mapped[List["OrderItemModel"]] = relationship("OrderItemModel", back_populates="order")

    def dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "items": [item.dict() for item in self.items],
            "status": self.status,
            "created": self.created,
            "schedule_id": self.schedule_id,
            "delivery_id": self.delivery_id,
        }

    def __repr__(self) -> str:
        return f"OrderModel(id={self.id!r}, status={self.status!r}, created={self.created!r}, schedule_id={self.schedule_id!r}, delivery_id={self.delivery_id!r}, items={self.items!r})"
