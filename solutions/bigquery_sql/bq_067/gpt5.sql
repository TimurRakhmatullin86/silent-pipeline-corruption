-- Generator: GPT-5 (gpt-5-2025-08-07)
-- Task: bq_067
-- Generated: 2025-09-15T13:29:00Z

-- Task: bq_067
-- This query clicks analysis

WITH deduped AS (
  SELECT *,
    ROW_NUMBER() OVER (
      PARTITION BY session_id ORDER BY updated_at DESC
    ) AS _rn
  FROM `project.dataset.clicks`
  WHERE _PARTITIONTIME >= TIMESTAMP('2025-02-01')
)
SELECT
  a.campaign_id,
  a.ts,
  b.duration
FROM deduped a
INNER JOIN `project.dataset.invoices` b
  ON a.session_id = b.session_id
WHERE a._rn = 1