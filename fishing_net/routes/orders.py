from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5
from pydantic import BaseModel, field_serializer


class MQLTradeRequest(BaseModel):
    action: str
    magic: int
    order: int
    symbol: str
    volume: float
    price: float
    stoplimit: float
    sl: float
    tp: float
    deviation: int
    type: int
    type_filling: int
    type_time: int
    expiration: int
    comment: str
    position: int
    position_by: int

    @field_serializer("action", when_used="json")
    def serialize_action(self, value):
        return getattr(mt5, value.upper())

    @field_serializer("type", when_used="json")
    def serialize_type(self, value):
        return getattr(mt5, value.upper())

    @field_serializer("type_filling", when_used="json")
    def serialize_type_filling(self, value):
        return getattr(mt5, value.upper())

    @field_serializer("type_time", when_used="json")
    def serialize_type_time(self, value):
        return getattr(mt5, value.upper())


router = APIRouter(tags=["Orders"])


@router.get("/total")
def orders_total(body: MT5LoginCredentials = Depends(get_current_user)):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.orders_total()


@router.get("/info")
def orders_get(
    symbol: str = "",
    group: str = "",
    ticket: int = 0,
    body: MT5LoginCredentials = Depends(get_current_user),
):
    if all([symbol, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )

    if symbol:
        orders = mt5.orders_get(symbol=symbol)
    elif group:
        orders = mt5.orders_get(group=group)
    elif ticket:
        orders = mt5.orders_get(ticket=ticket)
    else:
        orders = mt5.orders_get()
    print(mt5.last_error())
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")
    print(orders)
    return orders


@router.get("/check/margin")
def order_calc_margin(
    action: str,
    symbol: str,
    volume: float,
    price: float,
    body: MT5LoginCredentials = Depends(get_current_user),
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    margin = mt5.order_calc_margin(getattr(mt5, action.upper()), symbol, volume, price)

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return margin


@router.get("/check/profit")
def order_calc_profit(
    action: str,
    symbol: str,
    volume: float,
    price_open: float,
    price_close: float,
    body: MT5LoginCredentials = Depends(get_current_user),
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    profit = mt5.order_calc_profit(
        getattr(mt5, action.upper()), symbol, volume, price_open, price_close
    )

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return profit


@router.post("/check")
def order_check(
    order_req: MQLTradeRequest,
    body: MT5LoginCredentials = Depends(get_current_user),
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    result = mt5.order_check(order_req.model_dump())
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return result
