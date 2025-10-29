from fastapi.testclient import TestClient
from app import main


client = TestClient(main.app)


def test_add_endpoint():
    r = client.get("/add", params={"a": 3, "b": 4})
    assert r.status_code == 200
    assert r.json()["result"] == 7


def test_div_by_zero_endpoint():
    r = client.get("/div", params={"a": 1, "b": 0})
    assert r.status_code == 400
    assert r.json()["detail"] == "division by zero"


def test_sub_endpoint():
    r = client.get("/sub", params={"a": 10, "b": 4})
    assert r.status_code == 200
    assert r.json()["result"] == 6


def test_mul_endpoint():
    r = client.get("/mul", params={"a": 3, "b": 5})
    assert r.status_code == 200
    assert r.json()["result"] == 15
