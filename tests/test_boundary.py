import pytest


@pytest.mark.parametrize("goods_id", [-1, 0])
def test_invalid_goods_id(api, fresh_stock, goods_id):
    """Negative or zero goods id must not create an order."""
    r = api.seckill(goods_id, 4001)
    body = r.json()
    assert body.get("success") is False, body


@pytest.mark.bug
@pytest.mark.xfail(reason="BUG-003: duplicate user sees success:true but no order is created", strict=True)
def test_duplicate_user_order(api, fresh_stock):
    """Same user ordering twice must be rejected at the API layer."""
    first = api.seckill(1, 5001).json()
    second = api.seckill(1, 5001).json()
    assert first["success"] is True
    assert second["success"] is False, "duplicate order accepted"
    assert second["message"] in ("duplicate order", "sold out")


def test_response_has_required_fields(api, fresh_stock):
    body = api.seckill(1, 6001).json()
    assert body["success"] is True
    assert "remain" in body
    assert isinstance(body["remain"], int)
