import pytest


@pytest.mark.smoke
def test_non_numeric_user_id_returns_400(api):
    """userId=abc must be rejected by type conversion, not 500."""
    r = api.seckill(1, "abc")
    assert r.status_code == 400, f"expected 400, got {r.status_code}"


@pytest.mark.smoke
def test_non_numeric_goods_id_returns_400(api):
    """goodsId=abc must be rejected by type conversion."""
    r = api.seckill("abc", 1)
    assert r.status_code == 400, f"expected 400, got {r.status_code}"


def test_empty_user_id_uses_default(api, fresh_stock):
    """No userId at all: endpoint has defaultValue=1, should still work."""
    r = api.session.post(f"{api.base_url}/seckill/1", timeout=10)
    assert r.status_code == 200
    assert "success" in r.json()
