from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user
from fishing_net.schemas import MQLSymbolTick
import MetaTrader5 as mt5
from datetime import datetime
import numpy as np
import pandas as pd

router = APIRouter(tags=["Ticks"])


@router.get("/history/{symbol}", dependencies=[Depends(get_current_user)])
def copy_ticks(
    symbol: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    count: int = 0,
) -> list[MQLSymbolTick]:
    if all([date_from, date_to, count]):
        return HTTPException(500, "Internal Server Error")

    if date_from and date_to:
        ticks = mt5.copy_ticks_range(symbol, date_from, date_to, mt5.COPY_TICKS_ALL)
    elif date_from and count:
        ticks = mt5.copy_ticks_from(symbol, date_from, count, mt5.COPY_TICKS_ALL)

    if not mt5.last_error()[0]:
        return HTTPException(500, "Internal Server Error")

    if not ticks.size:
        return HTTPException(500, "Internal Server Error")

    ticks = pd.DataFrame(ticks)

    return ticks.to_dict(orient="records")


@router.get("/current/{symbol}", dependencies=[Depends(get_current_user)])
def get_ticks(
    symbol: str,
) -> list[dict[str, MQLSymbolTick]]:
    if "*" not in symbol:
        tick_info = mt5.symbol_info_tick(symbol)

        if not mt5.last_error()[0]:
            return HTTPException(500, "Internal Server Error")

        return [{symbol: MQLSymbolTick(**tick_info._asdict())}]
    else:
        symbols = [x.name for x in mt5.symbols_get(symbol) if x]
        ticks_info: dict[str, MQLSymbolTick] = []

        for s in symbols:
            tick_data = mt5.symbol_info_tick(s)
            if not tick_data:
                continue
            tick_data = MQLSymbolTick(**tick_data._asdict())
            ticks_info.append({s: tick_data})
        if not ticks_info:
            return HTTPException(500, "Internal Server Error")

        return ticks_info
