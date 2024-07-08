from fastapi import APIRouter, Depends
from fishing_net.utils import get_current_user, MT5LoginCredentials
import MetaTrader5 as mt5

router = APIRouter(tags=["Account"])


@router.get("/")
def account_information(body: MT5LoginCredentials = Depends(get_current_user)):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.account_info()._asdict()


@router.get("/{property}")
def specific_account_property(
    property: str, body: MT5LoginCredentials = Depends(get_current_user)
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.account_info()._asdict()[property]
