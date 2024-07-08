from fastapi.testclient import TestClient
from fishing_net.schemas import MQLAccountInfo
import os


def test_get_account_info(generate_token: str, client: TestClient):
    account_info = client.get(
        "/account", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert account_info.status_code == 200
    assert account_info.json().keys() == MQLAccountInfo.__annotations__.keys()


def test_get_specific_account_info(generate_token: str, client: TestClient):
    account_info = client.get(
        "/account/login", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert account_info.status_code == 200
    assert account_info.json() == int(os.getenv("TRADING_ACCOUNT_ID"))
