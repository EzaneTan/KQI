-- load_market_data.sql
-- 1) Create staging table
CREATE TABLE IF NOT EXISTS market_data_staging (
  trade_date    DATE,
  symbol        TEXT,
  open_price    NUMERIC,
  high_price    NUMERIC,
  low_price     NUMERIC,
  close_price   NUMERIC,
  volume        NUMERIC
);

-- 2) Load from CSV (Postgres COPY example)
COPY market_data_staging
FROM '/path/to/market_data.csv'
WITH (FORMAT csv, HEADER true);

-- 3) Create production table partitioned by symbol or date
CREATE TABLE IF NOT EXISTS market_data (
  LIKE market_data_staging INCLUDING ALL
) PARTITION BY LIST (symbol);

-- (You’d then CREATE PARTITION market_data FOR VALUES IN (‘BTC’, ‘ETH’, …);)
