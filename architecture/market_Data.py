class MarketDataProvider:
    """
    Connects to on-chain or centralized exchange APIs to retrieve
    real-time and historical market data.
    """
    def __init__(self, sources: List[str], cache_dir: str = "./data/cache"):
        pass

    def fetch_live(self, symbol: str) -> Dict:
        """Return the latest tick data for a given symbol."""
        pass

    def fetch_historical(self, symbol: str, start: datetime, end: datetime) -> pd.DataFrame:
        """Return OHLCV or order-book snapshots over a time range."""
        pass

    def clear_cache(self):
        """Empty the local cache to free up disk or force fresh pulls."""
        pass
