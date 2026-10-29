import pytest

from api.seckill_api import SeckillApi


@pytest.fixture(scope="session")
def api():
    return SeckillApi()


@pytest.fixture()
def fresh_stock(api):
    """Reload stock from DB into Redis before each case that needs it."""
    api.reload_stock()
    yield