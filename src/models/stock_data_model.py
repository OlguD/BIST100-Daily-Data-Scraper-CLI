from datetime import datetime
from dataclasses import dataclass

@dataclass
class StockDataModel:
    stock_name: str
    date: datetime
    dollar_based_price: float
    index_based_price: float
    dollar_based_min_price: float
    dollar_based_max_price: float
    dollar_based_open_price: float
    open: float
    close: float
    high: float
    low: float
    volume: float

    def __str__(self):
        return {
            "name": self.stock_name,
            "date": self.date,
            "dollar_based_price": self.dollar_based_price,
            "index_based_price": self.index_based_price,
            "dollar_based_min_price": self.dollar_based_min_price,
            "dollar_based_max_price": self.dollar_based_max_price,
            "dollar_based_open_price": self.dollar_based_open_price,
            "open": self.open,
            "close": self.close,
            "high": self.high,
            "low": self.low,
            "volume": self.volume,
        }
    
    def to_dict(self):
        try:
            return {k: (v if not isinstance(v, float) else (round(v, 10) if v is not None else None))
                    for k, v in self.__dict__.items()}
        except Exception:
            return dict(self.__dict__)
        
    def __repr__(self):
        d = self.to_dict()
        return f"StockDataModel({d})"