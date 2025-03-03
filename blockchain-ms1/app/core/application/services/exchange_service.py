import requests
from app.core.domain.interfaces.exchange_provider import ExchangeProvider

class ExchangeService(ExchangeProvider):
    COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
    def get_exchange_rate(self, currency: str) -> float:
        """
        Fetches the exchange rate for Bitcoin and Ethereum in the specified currency.
        Supports USD, BRL, EUR, etc.
        """
        try:
            response = requests.get(self.COINGECKO_API_URL, params={
                "ids": "bitcoin,ethereum",
                "vs_currencies": currency.lower()

            })
            response.raise_for_status()
            data = response.json()
            return {
                "bitcoin": data.get("bitcoin", {}).get(currency.lower(), None),
                "ethereum": data.get("ethereum", {}).get(currency.lower(), None),
            }
        except requests.RequestException as e:
            print(f"Error fetching exchange rate: {e}")
            return {"error": "Unable to fetch exchange rate"}
