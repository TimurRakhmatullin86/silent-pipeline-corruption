-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_018
-- Generated: 2025-09-15T10:38:00Z

-- Task: bq_018
-- This query tickets analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.tickets`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-01-01')
)
SELECT
  a.session_id,
  a.ts,
  b.score
FROM deduped a
INNER JOIN `project.dataset.users` b
  ON a.customer_id = b.customer_id
WHERE a._rn = 1