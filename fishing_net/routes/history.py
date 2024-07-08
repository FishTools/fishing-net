from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5
from datetime import datetime
from fishing_net.schemas import MQLHistoryOrder, MQLHistoryDeal

router = APIRouter(tags=["History"])


@router.get("/orders/total", dependencies=[Depends(get_current_user)])
def history_orders_total() -> int:
    return mt5.history_orders_total()


@router.get("/orders/info", dependencies=[Depends(get_current_user)])
def history_orders_get(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    group: str = "",
    ticket: int = 0,
    position: int = 0,
) -> MQLHistoryOrder:
    if all([date_from, date_to, position, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

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

    return MQLHistoryOrder(**history_orders)


@router.get("/deals/total", dependencies=[Depends(get_current_user)])
def history_deals_total() -> int:
    return mt5.history_deals_total()


@router.get("/deals/info", dependencies=[Depends(get_current_user)])
def history_deals_get(
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    group: str = "",
    ticket: int = 0,
    position: int = 0,
) -> MQLHistoryDeal:
    if all([date_from, date_to, position, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

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

    return MQLHistoryDeal(**history_deals)
