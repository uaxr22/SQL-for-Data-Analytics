-- Bronze quality checks
SELECT COUNT(*) AS null_record_id
FROM bronze.events
WHERE record_id IS NULL;

SELECT COUNT(*) AS null_source_system
FROM bronze.events
WHERE source_system IS NULL;

SELECT COUNT(*) AS null_ingest_ts
FROM bronze.events
WHERE ingest_ts IS NULL;

SELECT record_id, COUNT(*) AS dup_count
FROM bronze.events
GROUP BY record_id
HAVING COUNT(*) > 1;
