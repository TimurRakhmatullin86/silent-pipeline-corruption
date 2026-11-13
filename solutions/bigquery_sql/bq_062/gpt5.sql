-- Generator: gpt-5-2025-08-07
-- Task: bq_062
-- Generated: 2025-10-02T13:30:22Z

SELECT
  load_audit.table_name,
  load_audit.load_date,
  load_audit.row_count
FROM `project.dataset.load_audit` AS load_audit
JOIN `project.dataset.dq_config` AS dq_config
  ON load_audit.table_name = dq_config.table_name
WHERE load_audit.load_date >= '2025-01-01'
  AND load_audit.load_date < '2025-07-01'
ORDER BY 1