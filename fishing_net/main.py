from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import MetaTrader5 as mt5
from pydantic import BaseModel
import jwt
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError


mt5.initialize()
app = FastAPI()

SECRET_KEY = "sample data"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()


class MT5LoginCredentials(BaseModel):
    login: int
    password: str | None = None
    server: str | None = None
    timeout: int | None = None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> MT5LoginCredentials:
    """
    Retrieves the current user based on the provided credentials.

    Args:
        credentials (HTTPAuthorizationCredentials): The credentials used for authentication.

    Returns:
        MT5LoginCredentials: The current user's login credentials.

    Raises:
        HTTPException: If the credentials are invalid or could not be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        if not payload:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = MT5LoginCredentials(**payload)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create an access token with the provided data and expiration delta.

    Args:
        data (dict): The data to be encoded in the access token.
        expires_delta (timedelta | None, optional): The expiration delta for the access token.
            If not provided, a default expiration of 15 minutes will be used.

    Returns:
        str: The encoded access token.

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post(
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
def login(body: MT5LoginCredentials) -> str:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(403, f"Invalid Credentials {mt5.last_error()}")

    encrypted_key = create_access_token(
        body.model_dump(), timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return encrypted_key


@app.get(
    "/account",
    summary="Retrieves the account information for the specified user.",
    description="Retrieves the account information for the specified user, including the account balance, equity, margin, and other details.",
    response_model=dict,
    responses={200: {"description": "Successful operation"}},
)
def account_info(body: MT5LoginCredentials = Depends(get_current_user)) -> dict:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.account_info()._asdict()


@app.get(
    "/terminal",
    summary="Retrieves information about the MetaTrader 5 terminal.",
    description="Retrieves information about the MetaTrader 5 terminal, including the platform version, build number, and other details.",
    response_model=dict,
    responses={
        200: {"description": "Successful operation"},
        500: {"description": "Internal Server Error"},
    },
)
def terminal_info(body: MT5LoginCredentials = Depends(get_current_user)) -> dict:
    """
    Retrieves information about the MetaTrader 5 terminal.

    Args:
        body (MT5LoginCredentials): The login credentials of the user.

    Returns:
        dict: A dictionary containing the terminal information.

    Raises:
        HTTPException: If there is an internal server error.
    """
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")
    return mt5.terminal_info()._asdict()


@app.get(
    "/total_symbols",
    response_model=int,
    summary="Retrieves the total number of symbols available in the MetaTrader 5 platform.",
    description="Retrieves the total number of symbols available in the MetaTrader 5 platform.",
    responses={
        500: {"description": "Internal Server Error"},
        200: {"description": "Successful operation"},
    },
)
def symbols_total(body: MT5LoginCredentials = Depends(get_current_user)) -> int:
    """
    Retrieves the total number of symbols available in the MetaTrader 5 platform.

    Parameters:
    - body: MT5LoginCredentials - The login credentials of the user making the request.

    Returns:
    - int: The total number of symbols available.

    Raises:
    - HTTPException: If there is an internal server error.
    """
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")
    return mt5.symbols_total()


@app.get(
    "/version",
    response_model=dict,
    summary="Retrieves the version of the MetaTrader 5 platform.",
    description="Retrieves the version of the MetaTrader 5 platform.",
    responses={
        200: {"description": "Successful operation"},
        500: {"description": "Internal Server Error"},
    },
)
def version():
    version = mt5.version()

    if not version:
        raise HTTPException(500, "Internal Server Error")

    return {
        "terminal version": version[0],
        "build": version[1],
        "build date": version[2],
    }


@app.post(
    "/symbol_select",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Successful operation"},
        500: {"description": "Internal Server Error"},
    },
    summary="Enables or disables the specified symbol.",
    description="Enables or disables the specified symbol on the MetaTrader 5 platform.",
)
def symbol_select(
    symbol: str, enable: bool, body: MT5LoginCredentials = Depends(get_current_user)
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    mt5.symbol_select(symbol, enable)

    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    return {"symbol": symbol, "enabled": enable}


@app.get(
    "/symbols",
    response_model=dict,
    responses={
        200: {"description": "Successful operation"},
        500: {"description": "Internal Server Error"},
    },
    summary="Retrieves information about the specified symbol or group of symbols.",
    description="Retrieves information about the specified symbol or group of symbols. If a symbol is provided, the information for that symbol is returned. If a group is provided, the information for all symbols in that group is returned. If no symbol or group is provided, the information for all symbols is returned.",
)
def symbols_get(
    body: MT5LoginCredentials = Depends(get_current_user),
    symbol: str = "",
    group: str = "",
    all: bool = False,
):
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    if not group and not all and symbol:
        data = mt5.symbol_info(symbol.upper())._asdict()
        return {data["name"]: data}
    elif group and not symbol and not all:
        return [{x.name: x._asdict()} for x in mt5.symbols_get(group) if x]
    elif all and not symbol and not group:
        return [{x.name: x._asdict()} for x in mt5.symbols_get() if x]
    else:
        raise HTTPException(500, "Internal Server Error")


@app.get(
    "/tick",
    response_model=dict,
    responses={
        200: {"description": "Successful operation"},
        500: {"description": "Internal Server Error"},
    },
    summary="Retrieves tick information for the specified symbol or group of symbols.",
    description="Retrieves tick information for the specified symbol or group of symbols. If a symbol is provided, the tick information for that symbol is returned. If a group is provided, the tick information for all symbols in that group is returned. If no symbol or group is provided, the tick information for all symbols is returned.",
)
def symbols_tick(
    body: MT5LoginCredentials = Depends(get_current_user),
    symbol: str = "",
    group: str = "",
):
    """
    Get tick information for a symbol or a group of symbols.

    Parameters:
    - body: MT5LoginCredentials - The login credentials for the MetaTrader 5 server.
    - symbol: str - The symbol for which to retrieve tick information. If not provided, tick information for all symbols in the specified group will be returned.
    - group: str - The group of symbols for which to retrieve tick information. If not provided, tick information for the specified symbol will be returned.

    Returns:
    - dict or list of dict - The tick information for the specified symbol(s). If a single symbol is provided, a dictionary with the tick information is returned. If a group of symbols is provided, a list of dictionaries, each containing the tick information for a symbol, is returned.

    Raises:
    - HTTPException(500, "Internal Server Error") - If there is an internal server error while retrieving the tick information.
    """
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

    if all([symbol, group]):
        raise HTTPException(500, "Internal Server Error")

    if symbol:
        return mt5.symbol_info_tick(symbol)._asdict()
    else:
        symbols = [x.name for x in mt5.symbols_get(group) if x]
        return [{s: mt5.symbol_info_tick(s)} for s in symbols]
