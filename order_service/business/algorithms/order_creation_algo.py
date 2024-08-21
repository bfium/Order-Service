from utilities.data_mappers.database_wrappers.order_item_model import (
    OrderItemModel,
)
from order_service.entities.order import Order
from utilities.data_mappers.database_wrappers.order_model import OrderModel


class OrderCreationAlgo:
    @staticmethod
    def create(session, orders,user_id) -> Order:
        record = OrderModel(
            items=[OrderItemModel(**order) for order in orders],
            user_id=user_id
        )
        session.add(record)
        return Order(**record.dict(), order_=record)
