-- Generator: Claude Sonnet 4 (claude-sonnet-4-20250514)
-- Task: bq_031
-- Generated: 2025-09-15T12:06:03Z

SELECT
  account_id,
  COUNT(*) AS cnt,
  AVG(quantity) AS avg_val
FROM `project.dataset.transactions`
WHERE _PARTITIONTIME >= TIMESTAMP('2025-05-01')
GROUP BY account_id
HAVING avg_val > 0