-- Generator: gpt-5-2025-08-07
-- Task: bq_055
-- Generated: 2025-10-28T14:41:05Z

SELECT
  purchases_v1.event_uuid,
  purchases_v1.user_id,
  purchases_v1.ts,
  SUM(purchases_v1.amount_cents) AS total_amount_cents
FROM `project.dataset.purchases_v1` AS purchases_v1
JOIN `project.dataset.purchases_v2` AS purchases_v2
  ON purchases_v1.event_uuid = purchases_v2.event_uuid
GROUP BY 1, 2, 3
ORDER BY 1