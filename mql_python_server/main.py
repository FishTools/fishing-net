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
):
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


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/login")
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


@app.get("/account")
def account_info(body: MT5LoginCredentials = Depends(get_current_user)) -> dict:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    return mt5.account_info()._asdict()


@app.get("/terminal")
def terminal_info(body: MT5LoginCredentials = Depends(get_current_user)) -> dict:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")
    return mt5.terminal_info()._asdict()


@app.get("/total_symbols")
def symbols_total(body: MT5LoginCredentials = Depends(get_current_user)) -> int:
    mt5.login(
        body.login,
        password=body.password,
        server=body.server,
        timeout=body.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")
    return mt5.symbols_total()


@app.get("/symbols")
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


@app.get("/tick")
def symbols_tick(
    body: MT5LoginCredentials = Depends(get_current_user),
    symbol: str = "",
    group: str = "",
):
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
