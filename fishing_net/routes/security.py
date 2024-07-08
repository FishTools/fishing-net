from fastapi import HTTPException, status, APIRouter
from datetime import timedelta
from fishing_net.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    MQLLoginCredentials,
)
import MetaTrader5 as mt5

router = APIRouter(tags=["Security"])


@router.post(
    "/login",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Login to the MetaTrader 5 platform.",
    description="Login to the MetaTrader 5 platform using the provided credentials.",
    responses={
        200: {"description": "Successful operation"},
        403: {"description": "Invalid Credentials"},
    },
)
def login(body: MQLLoginCredentials) -> str:
    if not mt5.last_error()[0]:
        raise HTTPException(403, f"Invalid Credentials {mt5.last_error()}")

    encrypted_key = create_access_token(
        body.model_dump(), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return encrypted_key
