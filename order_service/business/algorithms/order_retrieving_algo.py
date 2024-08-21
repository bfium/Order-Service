from order_service.api.entities.exceptions import OrderNotFoundError
from order_service.entities.order import Order
from utilities.data_mappers.database_wrappers.order_model import OrderModel


class OrderRetrievingAlgo:
    @staticmethod
    def retrieve_by_id(self, session, id_, **filters) -> Order:
        order = (self.session.query(OrderModel)
                 .filter(OrderModel.id == str(id_))
                 .filter_by(**filters)
                 .first())
        if order is not None:
            return Order(**order.dict())
        raise OrderNotFoundError(f"Order {id_} not found")
