from abc import ABC


class OrderServiceInterface(ABC):
    def place_order(self, orders, user_id):
        pass

    def get_order_by_id(self, order_id, **filters):
        pass

    def delete_order(self, order_id):
        pass

    def update_order(self, order_id, items):
        pass

    def list_orders(self, **filters):
        pass

    def pay_order(self, order_id):
        pass

    def cancel_order(self, order_id):
        pass
