-- Generator: deepseek-chat-v3-0324
-- Task: bq_049
-- Generated: 2025-10-27T16:05:41Z

SELECT
  visits.visit_id,
  visits.patient_id,
  visits.visit_ts
FROM `project.dataset.visits` AS visits
JOIN `project.dataset.patients` AS patients
  ON visits.patient_id = patients.patient_id