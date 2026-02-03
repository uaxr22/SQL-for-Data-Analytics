-- Silver quality checks
-- Check: order_id should never be NULL.
SELECT COUNT(*) AS null_order_id
FROM silver.orders
WHERE order_id IS NULL;

-- Check: customer_id should never be NULL.
SELECT COUNT(*) AS null_customer_id
FROM silver.orders
WHERE customer_id IS NULL;

-- Check: order_date should never be NULL.
SELECT COUNT(*) AS null_order_date
FROM silver.orders
WHERE order_date IS NULL;

-- Check: order_id should be unique.
SELECT order_id, COUNT(*) AS dup_count
FROM silver.orders
GROUP BY order_id
HAVING COUNT(*) > 1;
