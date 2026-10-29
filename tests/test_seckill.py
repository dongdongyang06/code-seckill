import json
import os

import pytest

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "seckill_cases.json")


def load_cases():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)["seckill_cases"]


CASES = load_cases()


# ---------- GET /goods ----------

@pytest.mark.smoke
def test_list_goods_returns_200(api):
    r = api.list_goods()
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.smoke
def test_list_goods_contains_item(api):
    r = api.list_goods()
    goods = r.json()
    assert len(goods) >= 1
    for field in ("id", "name", "price", "stock"):
        assert field in goods[0], f"missing field: {field}"


# ---------- POST /seckill ----------

@pytest.mark.smoke
@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_seckill_by_data(api, fresh_stock, case):
    r = api.seckill(case["goods_id"], case["user_id"])
    body = r.json()
    assert body["success"] is case["expect_success"], body


def test_seckill_decreases_remain(api, fresh_stock):
    r1 = api.seckill(1, 2001)
    r2 = api.seckill(1, 2002)
    assert r1.json()["remain"] - 1 == r2.json()["remain"]


# ---------- known defects (BUG-001 / BUG-002) ----------

@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-001: non-existent goods returns 200 instead of 404", strict=True)
def test_missing_goods_should_return_4xx(api):
    r = api.seckill(99999, 3001)
    assert r.status_code == 404, f"expected 404, got {r.status_code}: {r.text}"


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-002: non-existent order returns 200 with empty body instead of 404", strict=True)
def test_missing_order_should_return_404(api):
    r = api.get_order(9999999)
    assert r.status_code == 404, f"expected 404, got {r.status_code}: {r.text}"