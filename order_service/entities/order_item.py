class OrderItem:
    def __init__(self, id, product, quantity, size):
        self.id = id
        self.product = product
        self.quantity = quantity
        self.size = size

    def dict(self):
        return {
            'product': self.product,
            'size': self.size,
            'quantity': self.quantity
        }

