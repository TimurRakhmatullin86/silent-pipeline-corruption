-- Generator: claude-sonnet-4-20250514
-- Task: bq_052
-- Generated: 2025-10-07T11:24:26Z

SELECT touches.touch_id, touches.user_id, touches.channel
FROM `project.dataset.touches` AS touches
JOIN `project.dataset.conversions` AS conversions
  ON touches.user_id = conversions.user_id