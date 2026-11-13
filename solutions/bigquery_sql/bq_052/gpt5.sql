-- Generator: gpt-5-2025-08-07
-- Task: bq_052
-- Generated: 2025-08-19T11:33:26Z

SELECT
  touches.touch_id,
  touches.user_id,
  touches.channel
FROM `project.dataset.touches` AS touches
JOIN `project.dataset.conversions` AS conversions
  ON touches.user_id = conversions.user_id
ORDER BY 1