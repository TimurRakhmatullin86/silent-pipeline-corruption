-- Generator: deepseek-chat-v3-0324
-- Task: bq_034
-- Generated: 2025-09-12T12:29:41Z

SELECT
  temperature_readings.device_id,
  temperature_readings.reading_ts,
  temperature_readings.temperature
FROM `project.dataset.temperature_readings` AS temperature_readings
JOIN `project.dataset.devices` AS devices
  ON temperature_readings.device_id = devices.device_id