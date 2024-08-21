# test/test_order_service.py
import pytest
from unittest.mock import Mock
from order_service.order_service import OrderService


@pytest.fixture
def orders_manager():
    return Mock()


@pytest.fixture
def order_service(orders_manager):
    return OrderService(orders_manager)


def test_place_order(order_service, orders_manager):
    orders = [{'id': '123', 'product': 'Book', 'quantity': 1}]

    orders_manager.place_order.return_value = 'Order placed'

    result = order_service.place_order(orders)

    orders_manager.place_order.assert_called_once_with(orders)
    assert result == 'Order placed'
