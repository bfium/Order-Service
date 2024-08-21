import uuid
from http import HTTPStatus
from pathlib import Path
from typing import Optional, Annotated, Union

import yaml
from fastapi import FastAPI, HTTPException, Query, Depends
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from order_service.api.entities.exceptions import OrderNotFoundError
from order_service.api.mutations.create_order_request_mutation import (
    CreateOrderRequestMutation,
)
from order_service.api.queries.get_orders_query import GetOrdersQuery
from order_service.business.managers.orders_manager import OrdersManager
from order_service.order_service import OrderService
from utilities.data_authorization.authorize_request_middleware import AuthorizeRequestMiddleware
from utilities.data_mappers.from_sql_alchemy.atomic_transaction import (
    AtomicTransaction,
)

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


@api.get("/orders", response_model=GetOrdersQuery)
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
    response_model=CreateOrderRequestMutation,
)
async def create_order(request: Request, order_payload: GetOrdersQuery):
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


def common_parameters(q: str = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}


@api.get("/")
def read_items(q: Annotated[str, Query(max_length=50)] = None):
    return {"q": q}


@api.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


def common_parameters_v2(
    q: Annotated[str, Query(max_length=50)] = None,
    skip: int = 0,
    limit: int = 10
):
    return {"q": q, "skip": skip, "limit": limit}


@api.get("/items_v2/")
async def read_items(commons: dict = Depends(common_parameters_v2)):
    return commons


@api.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^fixedquery$"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
