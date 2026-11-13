-- Generator: DeepSeek-V3 (deepseek-chat-v3-0324)
-- Task: bq_065
-- Generated: 2025-09-15T13:21:54Z

SELECT
  channel,
  ts,
  clicks,
  ROW_NUMBER() OVER (
    PARTITION BY channel
    ORDER BY clicks DESC
  ) AS rn,
  SUM(clicks) OVER (
    PARTITION BY channel
    ORDER BY ts
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM `project.dataset.sessions`
WHERE _PARTITIONTIME >= timestamp('2025-06-01')
  AND channel IS NOT NULL