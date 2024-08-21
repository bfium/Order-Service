from order_service.order_service_interface import OrderServiceInterface


class OrderService(OrderServiceInterface):
    def __init__(self, orders_manager):
        self.orders_manager = orders_manager

    def get_order_by_id(self, order_id, **filters):
        pass

    def place_order(self, orders, user_id):
        return self.orders_manager.add_orders(orders, user_id)

    def delete_order(self, order_id):
        return self.orders_manager.delete_order(order_id)

    def update_order(self, order_id, items):
        pass

    def list_orders(self, **filters):
        pass

    def pay_order(self, order_id):
        pass

    def cancel_order(self, order_id):
        pass
