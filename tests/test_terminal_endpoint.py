from fastapi.testclient import TestClient
from fishing_net.schemas import MQLTerminalInfo


def test_get_terminal_info(client: TestClient):
    terminal_info = client.get("/terminal")
    assert terminal_info.status_code == 200
    assert terminal_info.json().keys() == MQLTerminalInfo.__annotations__.keys()


def test_get_specific_terminal_info(client: TestClient):
    terminal_info = client.get("/terminal/connected")
    assert terminal_info.status_code == 200
    assert terminal_info.json()


def test_get_terminal_version(client: TestClient):
    terminal_info = client.get("/terminal/version")
    assert terminal_info.status_code == 200
    assert list(terminal_info.json().keys()) == [
        "terminal_version",
        "build",
        "build_date",
    ]
