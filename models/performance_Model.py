from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any

@dataclass
class PerformanceModel:
    """
    Captures backtest or live‐run performance metrics.
    """
    timestamp: datetime
    total_return: float
    volatility: float
    max_drawdown: float
    metrics: Dict[str, Any]

    def summary(self) -> Dict[str, Any]:
        """
        A flattened summary for logging or reporting.
        """
        return {
            "timestamp": self.timestamp.isoformat(),
            "total_return": self.total_return,
            "volatility": self.volatility,
            "max_drawdown": self.max_drawdown,
            **self.metrics,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict (ready for YAML/JSON)."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PerformanceModel":
        """Reconstruct from serialized dict."""
        ts = datetime.fromisoformat(data["timestamp"])
        # extract core fields
        core = {k: data[k] for k in ("total_return", "volatility", "max_drawdown")}
        # anything else goes into metrics
        extra = {k: v for k, v in data.items() if k not in core and k != "timestamp"}
        return cls(timestamp=ts, metrics=extra, **core)
