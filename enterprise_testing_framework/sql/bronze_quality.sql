-- Bronze quality checks
-- Check: record_id should never be NULL.
SELECT COUNT(*) AS null_record_id
FROM bronze.events
WHERE record_id IS NULL;

-- Check: source_system should never be NULL.
SELECT COUNT(*) AS null_source_system
FROM bronze.events
WHERE source_system IS NULL;

-- Check: ingest_ts should never be NULL.
SELECT COUNT(*) AS null_ingest_ts
FROM bronze.events
WHERE ingest_ts IS NULL;

-- Check: record_id should be unique.
SELECT record_id, COUNT(*) AS dup_count
FROM bronze.events
GROUP BY record_id
HAVING COUNT(*) > 1;
