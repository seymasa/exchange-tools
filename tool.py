from maistro.core.base_tool import BaseTool
import requests
from decouple import config
from typing import Dict, Any


class ExchangeRateTool(BaseTool):
    name: str = "exchange_rate"
    description: str = "Verilen baz para biriminden diğer para birimlerine güncel döviz kuru bilgisi getirir."

    def _run(self, base_currency: str, target_currency: str) -> str:
        # 🔍 ENV TEST: python-decouple ile ortam değişkenlerini kontrol et
        http_proxy = config("HTTP_PROXY", default=None)
        https_proxy = config("HTTPS_PROXY", default=None)
        ca_bundle = config("REQUESTS_CA_BUNDLE", default=None)

        print("=== ENVIRONMENT CHECK ===")
        print(f"HTTP_PROXY: {http_proxy}")
        print(f"HTTPS_PROXY: {https_proxy}")
        print(f"REQUESTS_CA_BUNDLE: {ca_bundle}")
        print("==========================")

        url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        print('hey')

        if resp.status_code != 200 or data.get("result") != "success":
            return "Döviz kuru bilgisi alınamadı."

        rates = data.get("rates", {})
        target_rate = rates.get(target_currency.upper())
        if not target_rate:
            return f"{target_currency.upper()} kuru bulunamadı."

        return f"1 {base_currency.upper()} = {target_rate} {target_currency.upper()}"

    async def _arun(self, base_currency: str, target_currency: str) -> str:
        return self._run(base_currency, target_currency)
