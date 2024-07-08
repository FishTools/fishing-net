from fastapi.testclient import TestClient


def test_get_symbol_total(generate_token: str, client: TestClient):
    total_symbols = client.get(
        "/symbols/total", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert total_symbols.status_code == 200
    assert total_symbols.json()


def test_get_symbol_info_all(generate_token: str, client: TestClient):
    symbol_info = client.get(
        "/symbols/info?all=True", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert symbol_info.status_code == 200
    assert symbol_info.json()


def test_get_symbol_info_single(generate_token: str, client: TestClient):
    symbol_info = client.get(
        "/symbols/info?symbol=EURUSD",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert symbol_info.status_code == 200
    assert list(symbol_info.json().keys()) == ["EURUSD"]


def test_get_symbol_info_group(generate_token: str, client: TestClient):
    symbol_info = client.get(
        "/symbols/info?group=*USD*",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert symbol_info.status_code == 200
    assert symbol_info.json()
