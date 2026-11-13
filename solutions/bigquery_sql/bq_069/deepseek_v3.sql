-- Generator: deepseek-chat-v3-0324
-- Task: bq_069
-- Generated: 2025-08-30T13:49:09Z

SELECT
  raw_purchase_events.event_id,
  raw_purchase_events.source_id,
  raw_purchase_events.received_at
FROM `project.dataset.raw_purchase_events` AS raw_purchase_events
JOIN `project.dataset.event_sources` AS event_sources
  ON raw_purchase_events.source_id = event_sources.source_id