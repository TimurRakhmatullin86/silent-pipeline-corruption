-- Generator: deepseek-chat-v3-0324
-- Task: bq_029
-- Generated: 2025-08-12T11:52:28Z

SELECT
  carriers.carrier_id,
  carriers.carrier_name
FROM `project.dataset.carriers` AS carriers
JOIN `project.dataset.shipments` AS shipments
  ON carriers.carrier_id = shipments.carrier_id