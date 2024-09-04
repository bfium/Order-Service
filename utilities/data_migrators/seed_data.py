# seed_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from order_service.api.entities.size_enum import SizeEnum
from order_service.api.entities.status_enum import StatusEnum
from order_service.entities.order import Order
from order_service.entities.order_item import OrderItem

# Define the SQLite database URL
DB_URL = "sqlite:///orders.db"

# Create the engine and session
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Create some dummy data
order_items = [
    OrderItem(product="Product A", size=SizeEnum.small, quantity=2),
    OrderItem(product="Product B", size=SizeEnum.medium, quantity=1),
]

order = Order(
    status=StatusEnum.created,
    order=order_items
)

# Add and commit the data
session.add(order)
session.commit()

print("Dummy order inserted successfully!")
