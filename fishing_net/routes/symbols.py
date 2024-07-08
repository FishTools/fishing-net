from fastapi import APIRouter, Depends, HTTPException
from fishing_net.utils import get_current_user
import MetaTrader5 as mt5

router = APIRouter(tags=["Symbol"])


@router.get("/total", dependencies=[Depends(get_current_user)])
def total_symbols():
    total = mt5.symbols_total()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return total


@router.put("/select", dependencies=[Depends(get_current_user)])
def select_symbol(
    symbol: str,
    enable: bool,
):
    enabled_symbol = mt5.symbol_select(symbol, enable)

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return {"symbol": symbol, "enabled": enabled_symbol}


@router.get("/info", dependencies=[Depends(get_current_user)])
def symbols_info(
    symbol: str = "",
    group: str = "",
    all: bool = False,
):
    if not group and not all and symbol:
        data = mt5.symbol_info(symbol.upper())._asdict()
        return {data["name"]: data}
    elif group and not symbol and not all:
        return [{x.name: x._asdict()} for x in mt5.symbols_get(group) if x]
    elif all and not symbol and not group:
        return [{x.name: x._asdict()} for x in mt5.symbols_get() if x]
    else:
        raise HTTPException(500, "Internal Server Error")
