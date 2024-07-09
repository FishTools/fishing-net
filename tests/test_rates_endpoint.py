from fastapi.testclient import TestClient


def test_get_rates_from(generate_token: str, client: TestClient):
    rates = client.get(
        "/rates/EURUSD?timeframe=TIMEFRAME_D1&date_from=2024-07-09&count=10",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert rates.status_code == 200
    assert list(rates.json()[0].keys()) == [
        "time",
        "open",
        "high",
        "low",
        "close",
        "tick_volume",
        "spread",
        "real_volume",
    ]


def test_get_rates_range(generate_token: str, client: TestClient):
    rates = client.get(
        "/rates/EURUSD?timeframe=TIMEFRAME_D1&date_from=2024-06-09&date_to=2024-07-09",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert rates.status_code == 200
    assert list(rates.json()[0].keys()) == [
        "time",
        "open",
        "high",
        "low",
        "close",
        "tick_volume",
        "spread",
        "real_volume",
    ]


def test_get_rates_from_pos(generate_token: str, client: TestClient):
    rates = client.get(
        "/rates/EURUSD?timeframe=TIMEFRAME_D1&start_pos=10&count=10",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert rates.status_code == 200
    assert list(rates.json()[0].keys()) == [
        "time",
        "open",
        "high",
        "low",
        "close",
        "tick_volume",
        "spread",
        "real_volume",
    ]
