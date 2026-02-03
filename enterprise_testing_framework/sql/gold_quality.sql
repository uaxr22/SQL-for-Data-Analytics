-- Gold quality checks
-- Check: metric_date should never be NULL.
SELECT COUNT(*) AS null_metric_date
FROM gold.daily_sales
WHERE metric_date IS NULL;

-- Check: metric_name should never be NULL.
SELECT COUNT(*) AS null_metric_name
FROM gold.daily_sales
WHERE metric_name IS NULL;

-- Check: metric_value should never be NULL.
SELECT COUNT(*) AS null_metric_value
FROM gold.daily_sales
WHERE metric_value IS NULL;
