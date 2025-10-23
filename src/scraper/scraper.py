import requests
from datetime import datetime
import json
from utils.get_user_agent import get_random_user_agent
from models.stock_data_model import StockDataModel
from stocks import SYMBOLS
from concurrent.futures import ThreadPoolExecutor, as_completed


MAX_THREADS = 15

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        ua = get_random_user_agent()
        self.headers = {
            "Referer": "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Tarihsel-Fiyat-Bilgileri.aspx",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": ua,
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Origin": "https://www.isyatirim.com.tr"
        }

        # apply to session so subsequent requests reuse same headers and cookies
        self.session.headers.update(self.headers)
        self.session.get("https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Tarihsel-Fiyat-Bilgileri.aspx", timeout=10)


    def fetch_data(self, symbol: str, start_date, end_date = datetime.now().strftime("%d-%m-%Y")) -> json:
        try:
            url = f"https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse={symbol}&startdate={start_date}&enddate={end_date}"
            print(url)
            response = self.session.get(url, timeout=30, headers=self.headers, allow_redirects=True)

            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"Invalid json syntax: {e}\nResponse text (truncated): {response.text[:500]}")
                return None

            if response.ok:
                # print(data["value"])
                return data["value"]
            else:
                print(f"Non-OK response: {response.status_code}")
                return data

        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        

    def fetch_multiple_symbols(self, start_date, end_date = datetime.now().strftime("%d-%m-%Y")) -> json:
        symbols = SYMBOLS
        symbol_list = [symbol_name["symbol"] for symbol_name in symbols]

        results = {}

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(self.fetch_data, sym, start_date, end_date): sym for sym in symbol_list}
            for fut in as_completed(futures):
                sym = futures[fut]
                try:
                    results[sym] = fut.result()
                except Exception as e:
                    print(f"Error fecthing {sym}: {e}")
                    results[sym] = None

        return results

    def process_data(self, data) -> dict:
        if not data:
            print("process_data: invalid or empty data")
            return {"data": None, "status": False}

        def to_float(v):
            try:
                return float(v) if v is not None else None
            except (ValueError, TypeError):
                return None

        results = []
        items = data if isinstance(data, list) else [data]

        for item in items:
            try:
                stock_model = StockDataModel(
                    stock_name = item.get("HGDG_HS_KODU"),
                    date = item.get("HGDG_TARIH"),
                    dollar_based_price = to_float(item.get("DOLAR_BAZLI_FIYAT")),
                    index_based_price = to_float(item.get("ENDEKS_BAZLI_FIYAT")),
                    dollar_based_min_price = to_float(item.get("DOLAR_BAZLI_MIN")),
                    dollar_based_max_price = to_float(item.get("DOLAR_BAZLI_MAX")),
                    dollar_based_open_price = to_float(item.get("DOLAR_BAZLI_AOF")),
                    open = to_float(item.get("HGDG_AOF")),
                    close = to_float(item.get("HGDG_KAPANIS")),
                    high = to_float(item.get("HGDG_MAX")),
                    low = to_float(item.get("HGDG_MIN")),
                    volume = to_float(item.get("HGDG_HACIM")),
                )
                results.append(stock_model)
            except KeyError as e:
                print(f"Missing excepted key in items: {e}")
                continue

            except Exception as e:
                print(f"Error processing item: {e}")
                continue
            
        status = len(results) > 0
        return {
            "data": results,
            "status": status
        }