import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID
import yaml
from fastapi import FastAPI, HTTPException
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response


from order_service.api.schemas.schemas import GetOrderSchema, CreateOrderSchema, GetOrdersSchema
from utilities.data_authorization.authorize_request_middleware import AuthorizeRequestMiddleware

api = FastAPI(debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders")
oas_doc = yaml.safe_load(
    (Path(__file__).parent / "specifications/oas.yaml").read_text()
)

api.openapi = lambda: oas_doc
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.add_middleware(AuthorizeRequestMiddleware)

orders = [
        {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "created": "2024-09-03T12:34:56Z",
          "status": "dispatched",
          "order": [
            {
              "product": "capuccino",
              "size": "medium",
              "quantity": 10
            }
          ]
        },
        {
          "id": "550e8400-e29b-41d4-a716-446655440001",
          "created": "2024-09-03T12:36:22Z",
          "status": "cancelled",
          "order": [
            {
              "product": "milk",
              "size": "medium",
              "quantity": 1
            }
          ]
        },
        {
          "id": "550e8400-e29b-41d4-a716-446655440002",
          "created": "2024-09-03T12:40:12Z",
          "status": "created",
          "order": [
            {
              "product": "Laptop",
              "size": "medium",
              "quantity": 2
            },
            {
              "product": "Phone",
              "size": "small",
              "quantity": 1
            }
          ]
        }
      ]

"""

@api.get("/orders/{order_id}", response_model=OrderItemOut)
def get_order(order_id: uuid.UUID):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")


@api.get("/orders", response_model=GetOrders)
async def get_orders(request: Request, cancelled: Optional[bool] = None, limit: Optional[int] = None):
    with AtomicTransaction() as transaction:
        manager = OrdersManager(transaction.session)
        order_service = OrderService(manager)

        r_orders = order_service.list_orders(
            cancelled=cancelled,
            limit=limit,
            user_id=request.state.user_id
        )

    return {"orders": [order.dict() for order in r_orders]}


@api.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateOrder,
)
async def create_order(request: Request, order_payload: GetOrders):
    with AtomicTransaction() as transaction:
        manager = OrdersManager(transaction.session)
        order_service = OrderService(manager)

        order_ = order_payload.dict()["order"]
        for order in order_:
            order["size"] = order["size"].value
        order_creation_response = order_service.place_order(order_, request.state.user_id)
        transaction.commit()
        order_response_payload = order_creation_response.dict()
    return order_response_payload


@api.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: uuid.UUID):
    try:
        with AtomicTransaction() as transaction:
            manager = OrdersManager(transaction.session)
            order_service = OrderService(manager)
            order_service.delete_order(order_id=order_id)
            transaction.commit()
    except OrderNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

"""

@api.get("/orders", response_model=GetOrdersSchema)
def get_orders(cancelled: Optional[bool] = None, limit: Optional[int] = None):
    if cancelled is None and limit is None:
        return {"orders": orders}

    query_set = [order for order in orders]

    if cancelled is not None:
        if cancelled:
            query_set = [order for order in query_set if order["status"] == "cancelled"]
        else:
            query_set = [order for order in query_set if order["status"] != "cancelled"]

    if limit is not None and len(query_set) > limit:
        return {"orders": query_set[:limit]}

    return {"orders": query_set}


@api.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order: CreateOrderSchema):
    order = order.dict()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.utcnow()
    order["status"] = "created"
    orders.append(order)
    return order


@api.get("/orders/{order_id}", response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")


@api.put("/orders/{order_id}", response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for order in orders:
        if order["id"] == order_id:
            order.update(order_details)
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")


@api.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(index)
            return
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")


@api.post("/orders/{order_id}/cancel", response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "cancelled"
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")


@api.post("/orders/{order_id}/pay", response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "paid"
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
