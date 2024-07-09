from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd
from fishing_net.schemas import MQLSymbolRates

router = APIRouter(tags=["Rates"])


@router.get("/{symbol}", dependencies=[Depends(get_current_user)])
def copy_rates(
    symbol: str,
    timeframe: str,
    date_from: str = "",
    date_to: str = "",
    start_pos: int = 0,
    count: int = 0,
) -> list[MQLSymbolRates] | list:
    if all([date_from, date_to, count, start_pos]):
        raise HTTPException(500, "Internal Server Error")

    if date_from and date_to:
        rates = mt5.copy_rates_range(
            symbol,
            getattr(mt5, timeframe),
            datetime.fromisoformat(date_from),
            datetime.fromisoformat(date_to),
        )
    elif date_from and count:
        rates = mt5.copy_rates_from(
            symbol,
            getattr(mt5, timeframe),
            datetime.fromisoformat(date_from),
            count,
        )
    elif start_pos and count:
        rates = mt5.copy_rates_from_pos(
            symbol, getattr(mt5, timeframe), start_pos, count
        )
    else:
        raise HTTPException(500, "Internal Server Error")

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    rates = pd.DataFrame(rates).to_dict(orient="records")

    return rates
