-- feature_engineering.sql
WITH base AS (
  SELECT
    trade_date,
    symbol,
    close_price,
    daily_return
  FROM market_returns
),
sma AS (
  SELECT
    *,
    AVG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) AS sma_10,
    AVG(close_price) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) AS sma_50
  FROM base
),
rsi AS (
  SELECT
    *,
    100 - (100 / (1 +
      SUM(GREATEST(daily_return, 0)) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW)
      /
      SUM(ABS(LEAST(daily_return, 0))) OVER (PARTITION BY symbol ORDER BY trade_date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW)
    )) AS rsi_14
  FROM sma
)
SELECT * INTO market_features FROM rsi;
