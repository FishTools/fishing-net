from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5
from fishing_net.schemas import MQLOrder, MQLTradeRequest


router = APIRouter(tags=["Orders"])


@router.get("/total", dependencies=[Depends(get_current_user)])
def orders_total() -> int:
    total_order = mt5.orders_total()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return total_order


@router.get("/info", dependencies=[Depends(get_current_user)])
def orders_get(
    symbol: str = "",
    group: str = "",
    ticket: int = 0,
) -> MQLOrder | list[MQLOrder]:
    if all([symbol, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

    if symbol:
        orders = mt5.orders_get(symbol=symbol)
    elif group:
        orders = mt5.orders_get(group=group)
    elif ticket:
        orders = mt5.orders_get(ticket=ticket)
    else:
        orders = mt5.orders_get()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    if type(orders) is list:
        return [MQLOrder(**order) for order in orders]
    else:
        return MQLOrder(**orders)


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
