class PortfolioManager:
    """
    Maintains an up-to-date book of positions across strategies and protocols,
    computes total exposure, and can suggest rebalances.
    """
    def __init__(self):
        pass

    def update_positions(self, fills: List[Dict]):
        """Ingest fills/trades and update current holdings."""
        pass

    def compute_exposure(self) -> Dict:
        """Return per-asset and aggregate exposure metrics."""
        pass

    def rebalance(self, target_allocations: Dict[str, float]):
        """Generate orders necessary to move from current to target weights."""
        pass
