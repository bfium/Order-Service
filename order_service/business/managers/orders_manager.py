import os

from order_service.api.entities.exceptions import OrderNotFoundError
from order_service.business.algorithms.order_creation_algo import OrderCreationAlgo
from order_service.business.algorithms.order_deletion_algo import OrderDeletionAlgo
from order_service.business.algorithms.order_retrieving_algo import OrderRetrievingAlgo


class OrdersManager:
    def __init__(self, session):
        self.session = session

    def get_order_by_id(self, user_id):
        pass

    def add_orders(self, orders, user_id):
        record = OrderCreationAlgo.create(self.session, orders, user_id)
        return record

    def delete_order(self, order_id):
        order = OrderRetrievingAlgo.retrieve_by_id(self.session, order_id)
        if order is not None:
            return OrderDeletionAlgo.delete(self.session, order_id)
        raise OrderNotFoundError(f"Order {order_id} not found")
