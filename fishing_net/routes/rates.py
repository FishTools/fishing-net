from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5
from datetime import datetime

router = APIRouter(tags=["Rates"])


@router.get("/{symbol}")
def copy_rates(
    symbol: str,
    timeframe: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    start_pos: int = 0,
    count: int = 0,
    _body: MT5LoginCredentials = Depends(get_current_user),
):
    if all([date_from, date_to, count, start_pos]):
        raise HTTPException(500, "Internal Server Error")

    if date_from and date_to:
        rates = mt5.copy_rates_range(
            symbol, getattr(mt5, timeframe), date_from, date_to
        )
    elif date_from and count:
        rates = mt5.copy_rates_from(
            symbol, getattr(mt5, timeframe), date_from, count, start_pos
        )
    elif start_pos and count:
        rates = mt5.copy_rates_from_pos(
            symbol, getattr(mt5, timeframe), start_pos, count
        )
    else:
        raise HTTPException(500, "Internal Server Error")

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return rates._asdict()
