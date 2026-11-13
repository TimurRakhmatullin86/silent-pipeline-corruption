-- Generator: deepseek-chat-v3-0324
-- Task: bq_004
-- Generated: 2025-08-06T13:50:03Z

SELECT
  sensor_readings.reading_id,
  sensor_readings.sensor_id,
  sensor_readings.reading_timestamp
FROM `project.dataset.sensor_readings` AS sensor_readings
WHERE sensor_readings.reading_timestamp >= '2025-01-01'
  AND sensor_readings.reading_timestamp < '2025-07-01'