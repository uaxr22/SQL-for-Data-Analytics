-- Silver quality checks
SELECT COUNT(*) AS null_order_id
FROM silver.orders
WHERE order_id IS NULL;

SELECT COUNT(*) AS null_customer_id
FROM silver.orders
WHERE customer_id IS NULL;

SELECT COUNT(*) AS null_order_date
FROM silver.orders
WHERE order_date IS NULL;

SELECT order_id, COUNT(*) AS dup_count
FROM silver.orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT COUNT(*) AS out_of_range_order_total
FROM silver.orders
WHERE order_total < 0 OR order_total > 1000000;

SELECT COUNT(*) AS orphan_customer_id
FROM silver.orders o
LEFT JOIN silver.customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
