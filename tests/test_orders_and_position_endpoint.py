from fastapi.testclient import TestClient
import MetaTrader5 as mt5
from fishing_net.schemas import MQLTradeRequest, MQLTradeCheckResult

position_id = {"position_id": 0}


def test_orders_check(client: TestClient, generate_token):
    lot = 0.01
    point = client.get(
        "/symbols/info?symbol=EURUSD",
        headers={"Authorization": f"Bearer {generate_token}"},
    ).json()["EURUSD"]["point"]
    price = client.get(
        "/ticks/current/EURUSD", headers={"Authorization": f"Bearer {generate_token}"}
    ).json()[0]["EURUSD"]["ask"]

    assert lot
    assert price
    assert point

    request = MQLTradeRequest(
        action=mt5.TRADE_ACTION_DEAL,
        symbol="EURUSD",
        volume=lot,
        type=mt5.ORDER_TYPE_BUY,
        price=price,
        sl=price - 100 * point,
        tp=price + 100 * point,
        deviation=10,
        magic=123456,
        comment="Test",
        type_time=mt5.ORDER_TIME_GTC,
        type_filling=mt5.ORDER_FILLING_IOC,
    )

    response = client.post(
        "/orders/check",
        json=request.model_dump(),
        headers={"Authorization": f"Bearer {generate_token}"},
    )

    assert list(response.json().keys()) == list(
        MQLTradeCheckResult.__annotations__.keys()
    )


def test_orders_send(client: TestClient, generate_token):
    lot = 0.01
    point = client.get(
        "/symbols/info?symbol=EURUSD",
        headers={"Authorization": f"Bearer {generate_token}"},
    ).json()["EURUSD"]["point"]
    price = client.get(
        "/ticks/current/EURUSD", headers={"Authorization": f"Bearer {generate_token}"}
    ).json()[0]["EURUSD"]["ask"]

    assert lot
    assert price
    assert point

    request = MQLTradeRequest(
        action=mt5.TRADE_ACTION_DEAL,
        symbol="EURUSD",
        volume=lot,
        type=mt5.ORDER_TYPE_BUY,
        price=price,
        sl=price - 100 * point,
        tp=price + 100 * point,
        deviation=10,
        magic=123456,
        comment="Test",
        type_time=mt5.ORDER_TIME_GTC,
        type_filling=mt5.ORDER_FILLING_IOC,
    )

    check_response = client.post(
        "/orders/check",
        json=request.model_dump(),
        headers={"Authorization": f"Bearer {generate_token}"},
    )

    assert list(check_response.json().keys()) == list(
        MQLTradeCheckResult.__annotations__.keys()
    )

    response = client.post(
        "/orders/send",
        json=check_response.json()["request"],
        headers={"Authorization": f"Bearer {generate_token}"},
    )

    assert (
        response.json()["retcode"] == mt5.TRADE_RETCODE_DONE
    ), f"Check your mt5 settings; retcode: {response.json()["retcode"]}"

    position_id["position_id"] = response.json()["order"]


def test_positions_total(client: TestClient, generate_token: str):
    positions_total = client.get(
        "/position/total", headers={"Authorization": f"Bearer {generate_token}"}
    )
    assert positions_total.status_code == 200
    assert positions_total.json() >= 1


def test_positions_get_info_by_symbol(client: TestClient, generate_token: str):
    positions_info = client.get(
        "/position/info?symbol=EURUSD",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert positions_info.status_code == 200
    for position in positions_info.json():
        if position["symbol"] == "EURUSD":
            assert position["ticket"] == position_id["position_id"]
            break


def test_position_get_info_by_group(client: TestClient, generate_token: str):
    positions_info = client.get(
        "/position/info?group=*USD*",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert positions_info.status_code == 200
    for position in positions_info.json():
        if position["symbol"] == "EURUSD":
            assert position["ticket"] == position_id["position_id"]
            break


def test_position_get_info_by_id(client: TestClient, generate_token: str):
    # get first the position id of the current order in this symbol
    positions_info = client.get(
        "/position/info?symbol=EURUSD",
        headers={"Authorization": f"Bearer {generate_token}"},
    )
    assert positions_info.status_code == 200
    for position in positions_info.json():
        if position["symbol"] == "EURUSD":
            # close the active position
            point = client.get(
                "/symbols/info?symbol=EURUSD",
                headers={"Authorization": f"Bearer {generate_token}"},
            ).json()["EURUSD"]["point"]
            price = client.get(
                "/ticks/current/EURUSD",
                headers={"Authorization": f"Bearer {generate_token}"},
            ).json()[0]["EURUSD"]["bid"]
            request = MQLTradeRequest(
                action=mt5.TRADE_ACTION_DEAL,
                symbol="EURUSD",
                position=position["ticket"],
                volume=position["volume"],
                type=mt5.ORDER_TYPE_SELL,
                price=price,
                sl=price + 100 * point,
                tp=price - 100 * point,
                deviation=10,
                magic=123456,
                comment="Test",
                type_time=mt5.ORDER_TIME_GTC,
                type_filling=mt5.ORDER_FILLING_IOC,
            )

            response = client.post(
                "/orders/send",
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {generate_token}"},
            )
            response.json()["retcode"] == mt5.TRADE_RETCODE_DONE
            break
