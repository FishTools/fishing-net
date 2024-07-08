from fastapi import APIRouter, Depends
from fishing_net.utils import get_current_user, MT5LoginCredentials
from fishing_net.schemas import MQLAccountInfo
import MetaTrader5 as mt5

router = APIRouter(tags=["Account"])


@router.get("/")
def account_information(
    body: MT5LoginCredentials = Depends(get_current_user),
) -> MQLAccountInfo:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return MQLAccountInfo(**mt5.account_info()._asdict())


@router.get("/{property}")
def specific_account_property(
    property: str, body: MT5LoginCredentials = Depends(get_current_user)
) -> float | int | str | bool:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return getattr(MQLAccountInfo(**mt5.account_info()._asdict()), property)
