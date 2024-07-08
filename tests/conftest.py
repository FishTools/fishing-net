import pytest
import MetaTrader5 as mt5
import dotenv
from fishing_net.main import app
import os
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def setup_before_tests():
    dotenv.load_dotenv()
    mt5.initialize()
    yield
    mt5.shutdown()


@pytest.fixture()
def generate_token(client: TestClient):
    response = client.post(
        "/security/login",
        json={
            "login": os.getenv("TRADING_ACCOUNT_ID"),
            "password": os.getenv("TRADING_ACCOUNT_PASSWORD"),
            "server": os.getenv("TRADING_ACCOUNT_SERVER"),
            "timeout": 0,
        },
    )
    return response.json()
