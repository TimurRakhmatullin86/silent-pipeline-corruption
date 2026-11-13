-- Generator: claude-sonnet-4-20250514
-- Task: bq_004
-- Generated: 2025-08-30T14:21:52Z

SELECT sensor_readings.reading_id, sensor_readings.sensor_id, sensor_readings.reading_timestamp
FROM `project.dataset.sensor_readings` AS sensor_readings
WHERE sensor_readings.reading_timestamp >= '2025-01-01'
  AND sensor_readings.reading_timestamp <= '2025-07-01'