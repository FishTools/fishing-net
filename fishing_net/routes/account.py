from fastapi import APIRouter, Depends
from fishing_net.utils import get_current_user
from fishing_net.schemas import MQLAccountInfo
import MetaTrader5 as mt5

router = APIRouter(tags=["Account"])


@router.get("/", dependencies=[Depends(get_current_user)])
def account_information() -> MQLAccountInfo:
    return MQLAccountInfo(**mt5.account_info()._asdict())


@router.get("/{property}", dependencies=[Depends(get_current_user)])
def specific_account_property(
    property: str,
) -> float | int | str | bool:
    return getattr(MQLAccountInfo(**mt5.account_info()._asdict()), property)
