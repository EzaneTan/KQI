-- Roll forward 70/30 split by date
WITH sorted AS (
  SELECT *, ROW_NUMBER() OVER (ORDER BY trade_date) AS rn
  FROM market_data
)
SELECT *
FROM sorted
WHERE rn <= (SELECT FLOOR(0.7 * MAX(rn)) FROM sorted)
  INTO training_data;
  
SELECT *
FROM sorted
WHERE rn > (SELECT FLOOR(0.7 * MAX(rn)) FROM sorted)
  INTO test_data;
