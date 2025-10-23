import pandas as pd
from typing import Iterable, Union, Dict, List
import os

class Export:
    DEFAULT_COLS=["StockName", "Date", "DollarBasedPrice", "IndexBasedPrice", "DollarBasedMinPrice",
                    "DollarBasedMaxPrice", "DollarBasedOpenPrice", "Open", "Close", "High", "Low", "Volume"]
    
    HEADER_MAP = {
        "stock_name": "StockName",
        "date": "Date",
        "dollar_based_price": "DollarBasedPrice",
        "index_based_price": "IndexBasedPrice",
        "dollar_based_min_price": "DollarBasedMinPrice",
        "dollar_based_max_price": "DollarBasedMaxPrice",
        "dollar_based_open_price": "DollarBasedOpenPrice",
        "open": "Open",
        "close": "Close",
        "high": "High",
        "low": "Low",
        "volume": "Volume",
    }
    
    @staticmethod
    def _to_dataframe(data: Union[Dict, Iterable[Dict], pd.DataFrame]) -> pd.DataFrame:
        if isinstance(data, pd.DataFrame):
            df = data.copy()
        else:
            rows: List[Dict] = [data] if isinstance(data, dict) else list(data)
            mapped = []
            for r in rows:
                if not isinstance(r, dict):
                    conv = getattr(r, "to_dict", None)
                    if callable(conv):
                        r = conv()
                    else:
                        r = getattr(r, "__dict__", r)
                row_out = {out_col: r.get(in_key) for in_key, out_col in Export.HEADER_MAP.items()}
                mapped.append(row_out)
            
            df = pd.DataFrame(mapped, columns=Export.DEFAULT_COLS)

        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

        return df
    
    @staticmethod
    def _format_floats_as_strings(df: pd.DataFrame, float_format: str) -> pd.DataFrame:
        float_cols = df.select_dtypes(include=["float"]).columns
        for c in float_cols:
            df[c] = df[c].apply(lambda x: format(x, float_format) if pd.notnull(x) else x)
        return df

    @staticmethod
    def export_to_excel(filepath: str, data: Union[Dict, Iterable[Dict], pd.DataFrame], sheet_name: str = "StockData", index: bool = False, date_format: str = "%d-%m-%Y", float_format: str | None = ".8g") -> None:
        base, ext = os.path.splitext(filepath)
        if ext.lower() != ".xlsx":
            filepath = f"{filepath}.xlsx" if ext == "" else f"{base}.xlsx"

        df = Export._to_dataframe(data)
        if "Date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["Date"]):
            df["Date"] = df["Date"].dt.strftime(date_format)

        if float_format:
            df = Export._format_floats_as_strings(df, float_format)

        df.to_excel(filepath, sheet_name=sheet_name, index=index, engine="openpyxl")
   
    @staticmethod
    def export_to_csv(filepath: str, data: Union[Dict, Iterable[Dict], pd.DataFrame], index: bool = False, date_format: str = "%d-%m-%Y", float_format: str | None = ".8g") -> None:
        base, ext = os.path.splitext(filepath)
        if ext.lower() != ".csv":
            filepath = f"{filepath}.csv" if ext == "" else f"{base}.csv"
            
        df = Export._to_dataframe(data)
        if "Date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["Date"]):
            df["Date"] = df["Date"].dt.strftime(date_format)

        if float_format:
            df = Export._format_floats_as_strings(df, float_format)

        df.to_csv(filepath, index=index)