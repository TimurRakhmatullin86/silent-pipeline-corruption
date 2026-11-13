-- Generator: gpt-5-2025-08-07
-- Task: bq_049
-- Generated: 2025-08-17T16:37:21Z

SELECT
  visits.visit_id,
  visits.patient_id,
  visits.visit_ts
FROM `project.dataset.visits` AS visits
JOIN `project.dataset.patients` AS patients
  ON visits.patient_id = patients.patient_id
ORDER BY 1