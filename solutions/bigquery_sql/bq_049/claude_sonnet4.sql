-- Generator: claude-sonnet-4-20250514
-- Task: bq_049
-- Generated: 2025-10-12T18:50:11Z

SELECT
  visits.status, visits.visit_id, visits.patient_id, visits.visit_ts
FROM `project.dataset.visits` AS visits
JOIN `project.dataset.patients` AS patients
  ON visits.patient_id = patients.patient_id