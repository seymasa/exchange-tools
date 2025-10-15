from maistro.core.base_tool import BaseTool
import requests
from decouple import config
import pandas as pd


class ExchangeRateTool(BaseTool):
    name: str = "exchange_rate"
    description: str = "Verilen baz para biriminden diğer para birimlerine güncel döviz kuru bilgisi getirir."

    def _run(self, base_currency: str, target_currency: str) -> str:
        # ENV değişkenlerini python-decouple ile oku
        http_proxy = config("HTTP_PROXY", default=None)
        https_proxy = config("HTTPS_PROXY", default=None)
        ca_bundle = config("REQUESTS_CA_BUNDLE", default=None)

        # API isteği
        url = f"https://open.er-api.com/v6/latest/{base_currency.upper()}"
        resp = requests.get(url, timeout=10, verify=False)
        data = resp.json()

        # ENV bilgilerini tek blok olarak hazırla
        env_info = (
            f"=== ENVIRONMENT CHECK ===\n"
            f"HTTP_PROXY: {http_proxy}\n"
            f"HTTPS_PROXY: {https_proxy}\n"
            f"REQUESTS_CA_BUNDLE: {ca_bundle}\n"
            f"==========================\n"
        )

        if resp.status_code != 200 or data.get("result") != "success":
            return env_info + "Döviz kuru bilgisi alınamadı."

        # Pandas test bloğu
        df = pd.DataFrame(list(data.get("rates", {}).items()), columns=["Currency", "Rate"])
        summary = df.head(5).to_string(index=False)

        target_rate = data.get("rates", {}).get(target_currency.upper())
        if not target_rate:
            return env_info + f"{target_currency.upper()} kuru bulunamadı."

        return (
            env_info
            + f"1 {base_currency.upper()} = {target_rate} {target_currency.upper()}\n\n"
            + "İlk 5 döviz kuru:\n"
            + summary
        )

    async def _arun(self, base_currency: str, target_currency: str) -> str:
        return self._run(base_currency, target_currency)
