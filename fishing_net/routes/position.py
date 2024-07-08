from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user
import MetaTrader5 as mt5

router = APIRouter(tags=["Position"])


@router.get("/total", dependencies=[Depends(get_current_user)])
def total_positions():
    total = mt5.positions_total()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return total


@router.get("/info", dependencies=[Depends(get_current_user)])
def positions_get(symbol: str = "", group: str = "", ticket: int = 0):
    if all([symbol, group, ticket]):
        raise HTTPException(500, "Internal Server Error")

    if symbol:
        positions = mt5.positions_get(symbol=symbol)
    elif group:
        positions = mt5.positions_get(group=group)
    elif ticket:
        positions = mt5.positions_get(ticket=ticket)
    else:
        positions = mt5.positions_get()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    positions = [p._asdict() for p in positions]

    return positions
