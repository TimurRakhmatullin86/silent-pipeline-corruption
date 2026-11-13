-- Generator: claude-sonnet-4-20250514
-- Task: bq_029
-- Generated: 2025-08-10T09:20:38Z

SELECT carriers.carrier_id, carriers.carrier_name
FROM `project.dataset.carriers` AS carriers
JOIN `project.dataset.shipments` AS shipments
  ON carriers.carrier_id = shipments.carrier_id