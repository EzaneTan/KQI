from dataclasses import dataclass, field
from typing import List, Dict
from .position_model import PositionModel

@dataclass
class PortfolioModel:
    """
    A collection of positions, plus simple PnL & exposure helpers.
    """
    positions: List[PositionModel] = field(default_factory=list)

    def add_position(self, pos: PositionModel):
        self.positions.append(pos)

    def remove_position(self, asset: str):
        self.positions = [p for p in self.positions if p.asset != asset]

    def update_price(self, asset: str, new_price: float):
        for p in self.positions:
            if p.asset == asset:
                p.current_price = new_price

    def total_pnl(self) -> float:
        """
        Sum of PnL across all positions (ignores positions with None current_price).
        """
        return sum(p.pnl() or 0.0 for p in self.positions)

    def exposure(self) -> Dict[str, float]:
        """
        Returns raw exposure per asset (quantity * current_price), 0 if no price.
        """
        exp: Dict[str, float] = {}
        for p in self.positions:
            if p.current_price is not None:
                exp[p.asset] = p.quantity * p.current_price
            else:
                exp[p.asset] = 0.0
        return exp
