from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fishing_net.schemas import MQLLoginCredentials
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
import MetaTrader5 as mt5

SECRET_KEY = "sample data"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> MQLLoginCredentials:
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
            jwt=credentials.credentials, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        if (
            datetime.fromtimestamp(payload["exp"]).timestamp()
            < datetime.now(timezone.utc).timestamp()
        ):
            raise credentials_exception
        if not payload:
            raise credentials_exception
    except InvalidTokenError as e:
        print(e)
        raise credentials_exception
    user = MQLLoginCredentials(**payload)
    if user is None:
        raise credentials_exception
    mt5.login(
        user.login,
        password=user.password,
        server=user.server,
        timeout=user.timeout,
    )
    if not mt5.last_error()[0]:
        raise HTTPException(500, "Internal Server Error")

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
