from fastapi.testclient import TestClient


def test_get_current_tick_single(generate_token: str, client: TestClient):
    tick_info = client.get(
        "/ticks/current/EURUSD", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert tick_info.status_code == 200
    assert tick_info.json()


def test_get_current_tick_group(generate_token: str, client: TestClient):
    tick_info = client.get(
        "/ticks/current/*USD*", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert tick_info.status_code == 200
    assert tick_info.json()


def test_get_current_tick_all(generate_token: str, client: TestClient):
    tick_info = client.get(
        "/ticks/current/*", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert tick_info.status_code == 200

    assert tick_info.json()


def test_get_history_tick_single_count(generate_token: str, client: TestClient):
    tick_info = client.get(
        "/ticks/history/EURUSD?date_from=2024-07-09&count=10",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert tick_info.status_code == 200
    assert tick_info.json()
