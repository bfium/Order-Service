class OrderDeletionAlgo:
    @staticmethod
    def delete(self, session, order_id):
        session.delete(order_id)
