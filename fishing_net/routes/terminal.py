from fastapi import APIRouter, HTTPException
import MetaTrader5 as mt5

router = APIRouter(tags=["Terminal"])


@router.get("/")
def terminal_information():
    terminal_info = mt5.terminal_info()._asdict()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return terminal_info


@router.get("/version")
def terminal_version():
    version = mt5.version()

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return {
        "terminal version": version[0],
        "build": version[1],
        "build date": version[2],
    }


@router.get("/{property}")
def specific_terminal_property(property: str):
    terminal_property = mt5.terminal_info()._asdict()[property]

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return terminal_property
