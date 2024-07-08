from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5
from datetime import datetime

router = APIRouter(tags=["Ticks"])


@router.get("/history/{symbol}")
def copy_ticks(
    symbol: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    count: int = 0,
    _body: MT5LoginCredentials = Depends(get_current_user),
):
    if all([date_from, date_to, count]):
        return HTTPException(500, "Internal Server Error")

    if date_from and date_to:
        ticks = mt5.copy_ticks_range(symbol, date_from, date_to, mt5.COPY_TICKS_ALL)
    elif date_from and count:
        ticks = mt5.copy_ticks_range(symbol, date_from, count, mt5.COPY_TICKS_ALL)

    if not mt5.last_error()[0]:
        return HTTPException(500, "Internal Server Error")

    return ticks._asdict()


@router.get("/current/{symbol}")
def get_ticks(
    symbol: str,
    _body: MT5LoginCredentials = Depends(get_current_user),
):
    if "*" not in symbol:
        tick_info = mt5.symbol_info_tick(symbol)

        if not mt5.last_error()[0]:
            return HTTPException(500, "Internal Server Error")

        return tick_info
    else:
        symbols = [
            x.name for x in mt5.symbols_get(symbol) if x and not mt5.last_error()[0]
        ]

        tick_info = [
            {s: mt5.symbol_info_tick(s)} for s in symbols and not mt5.last_error()[0]
        ]

        if not tick_info:
            return HTTPException(500, "Internal Server Error")

        return tick_info
