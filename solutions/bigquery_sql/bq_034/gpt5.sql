-- Generator: gpt-5-2025-08-07
-- Task: bq_034
-- Generated: 2025-08-08T08:13:19Z

SELECT
  temperature_readings.device_id,
  temperature_readings.reading_ts,
  temperature_readings.temperature
FROM `project.dataset.temperature_readings` AS temperature_readings
JOIN `project.dataset.devices` AS devices
  ON temperature_readings.device_id = devices.device_id
ORDER BY 1