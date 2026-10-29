from concurrent.futures import ThreadPoolExecutor

import pytest


@pytest.mark.slow
def test_no_oversell_under_concurrency(api, fresh_stock):
    """Fire (stock + 50) concurrent requests and assert exactly `stock` succeed.

    This is the automated version of the manual load test:
    it fails immediately if the deduction logic ever becomes non-atomic.
    """
    goods = api.list_goods().json()
    item = next(g for g in goods if g["id"] == 1)
    stock = item["stock"]
    assert stock > 0

    users = list(range(10000, 10000 + stock + 50))

    def buy(uid):
        try:
            return api.seckill(1, uid).json().get("success", False)
        except Exception:
            return False

    with ThreadPoolExecutor(max_workers=32) as pool:
        results = list(pool.map(buy, users))

    success = sum(1 for r in results if r)
    assert success == stock, f"expected {stock} success, got {success}"