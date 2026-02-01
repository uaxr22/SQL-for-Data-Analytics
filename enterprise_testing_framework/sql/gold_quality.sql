-- Gold quality checks
SELECT COUNT(*) AS null_metric_date
FROM gold.daily_sales
WHERE metric_date IS NULL;

SELECT COUNT(*) AS null_metric_name
FROM gold.daily_sales
WHERE metric_name IS NULL;

SELECT COUNT(*) AS null_metric_value
FROM gold.daily_sales
WHERE metric_value IS NULL;

SELECT COUNT(*) AS out_of_range_metric_value
FROM gold.daily_sales
WHERE metric_value < 0;
