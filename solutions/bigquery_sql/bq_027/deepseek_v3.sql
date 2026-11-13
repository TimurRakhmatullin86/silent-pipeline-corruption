-- Generator: deepseek-chat-v3-0324
-- Task: bq_027
-- Generated: 2025-10-26T15:23:23Z

SELECT
  shipments.shipment_id,
  shipments.order_id,
  shipments.warehouse_id
FROM `project.dataset.shipments` AS shipments
JOIN `project.dataset.warehouses` AS warehouses
  ON shipments.warehouse_id = warehouses.warehouse_id
JOIN `project.dataset.carriers` AS carriers
  ON shipments.carrier_id = carriers.carrier_id