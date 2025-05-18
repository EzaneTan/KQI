-- compute_returns.sql
CREATE TABLE IF NOT EXISTS market_returns AS
SELECT
  trade_date,
  symbol,
  close_price,
  LAG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date) AS prev_close,
  (close_price / LAG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date) - 1) AS daily_return
FROM market_data
ORDER BY symbol, trade_date;
