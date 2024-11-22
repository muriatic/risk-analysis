from abc import ABC, abstractmethod
from dataclasses import dataclass

import yfinance as yf # type : ignore
import pandas as pd # type : ignore

@dataclass
class Ticker:
    symbol: str
    name: str
    cusip: str

class Security(ABC):
    def __init__(self, ticker : Ticker) -> None:
        self._ticker : Ticker = ticker
        self._prices : pd.Series = None

    @property
    def prices(self) -> pd.Series:
        return self._prices
    
    @abstractmethod
    def percent_returns(self) -> pd.Series:
        pass

    @abstractmethod
    def price_returns(self) -> pd.Series:
        pass

class Equity(Security):
    def __init__(self, ticker : Ticker):
        super().__init__(ticker)
        self._prices = yf.Ticker(ticker.symbol).history(period="1y")["Close"]

    def percent_returns(self) -> pd.Series:
        return self._prices.pct_change()
    
    def price_returns(self) -> pd.Series:
        return self._prices.diff()