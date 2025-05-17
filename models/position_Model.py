from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class PositionModel:
    """
    Represents a single asset position in a portfolio.
    """
    asset: str
    quantity: float
    entry_price: float
    current_price: Optional[float] = None

    def pnl(self) -> Optional[float]:
        """
        Compute profit & loss for this position.
        Returns None if current_price is not set.
        """
        if self.current_price is None:
            return None
        return (self.current_price - self.entry_price) * self.quantity

    def to_dict(self) -> dict:
        """Serialize to a plain dict."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "PositionModel":
        """Deserialize from a dict."""
        return cls(
            asset=data["asset"],
            quantity=data["quantity"],
            entry_price=data["entry_price"],
            current_price=data.get("current_price"),
        )
