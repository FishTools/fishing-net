from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5
from datetime import datetime

router = APIRouter(tags=["History"])


@router.get("/orders/total")
def history_orders_total(
    body: MT5LoginCredentials = Depends(get_current_user),
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.history_orders_total()


@router.get("/orders/info")
def history_orders_get(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    group: str = "",
    ticket: int = 0,
    position: int = 0,
    body: MT5LoginCredentials = Depends(get_current_user),
):
    if all([date_from, date_to, position, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )

    if date_from and date_to and group:
        history_orders = mt5.history_orders_get(date_from, date_to, group=group)
    elif ticket:
        history_orders = mt5.history_orders_get(ticket=ticket)
    elif position:
        history_orders = mt5.history_orders_get(position=position)
    else:
        raise HTTPException(500, "Internal Server Error")

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return history_orders


@router.get("/deals/total")
def history_deals_total(
    body: MT5LoginCredentials = Depends(get_current_user),
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.history_deals_total()


@router.get("/deals/info")
def history_deals_get(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    group: str = "",
    ticket: int = 0,
    position: int = 0,
    body: MT5LoginCredentials = Depends(get_current_user),
):
    if all([date_from, date_to, position, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )

    if date_from and date_to and group:
        history_deals = mt5.history_deals_get(date_from, date_to, group=group)
    elif ticket:
        history_deals = mt5.history_deals_get(ticket=ticket)
    elif position:
        history_deals = mt5.history_deals_get(position=position)
    else:
        raise HTTPException(500, "Internal Server Error")

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return history_deals
