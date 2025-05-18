import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compute_sharpe(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Compute annualized Sharpe ratio for a series of returns.
    returns: periodic returns (e.g., daily)
    risk_free_rate: annualized risk-free rate
    """
    # Convert risk-free to same period
    rf_per_period = (1 + risk_free_rate) ** (1 / len(returns)) - 1
    excess_ret = returns - rf_per_period
    return np.sqrt(len(returns)) * excess_ret.mean() / excess_ret.std()


def compute_max_drawdown(equity: pd.Series) -> float:
    """
    Compute the maximum drawdown of an equity curve.
    equity: cumulative PnL or portfolio value series
    """
    cum_max = equity.cummax()
    drawdown = (equity - cum_max) / cum_max
    return drawdown.min()


def compute_win_loss_ratio(returns: pd.Series) -> float:
    """
    Compute win/loss ratio: number of positive returns over negative returns.
    """
    wins = (returns > 0).sum()
    losses = (returns < 0).sum()
    return wins / losses if losses > 0 else np.inf


def evaluate_agent(equity: pd.Series, title: str = "Agent Performance") -> dict:
    """
    Aggregate performance metrics and plot equity curve.
    Returns a dict of metrics.
    """
    # Compute periodic returns
    returns = equity.pct_change().dropna()

    sharpe = compute_sharpe(returns)
    max_dd = compute_max_drawdown(equity)
    wl_ratio = compute_win_loss_ratio(returns)
    total_return = equity.iloc[-1] / equity.iloc[0] - 1

    # Plot equity curve
    plt.figure(figsize=(10, 6))
    plt.plot(equity.index, equity.values)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_').lower()}_equity.png")
    plt.close()

    metrics = {
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "win_loss_ratio": wl_ratio,
        "total_return": total_return,
    }

    # Optionally print or log
    print("Performance met
