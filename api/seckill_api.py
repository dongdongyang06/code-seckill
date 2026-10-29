"""Thin wrapper around the seckill REST API.

Keeping HTTP details here means test cases read like plain English
and the API can be swapped without touching tests.
"""

import requests

from config import BASE_URL, TIMEOUT


class SeckillApi:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def list_goods(self):
        return self.session.get(f"{self.base_url}/goods", timeout=TIMEOUT)

    def seckill(self, goods_id, user_id):
        return self.session.post(
            f"{self.base_url}/seckill/{goods_id}",
            params={"userId": user_id},
            timeout=TIMEOUT,
        )

    def get_order(self, order_id):
        return self.session.get(f"{self.base_url}/order/{order_id}", timeout=TIMEOUT)

    def reload_stock(self):
        return self.session.post(f"{self.base_url}/admin/reload-stock", timeout=TIMEOUT)