-- Generator: claude-sonnet-4-20250514
-- Task: bq_050
-- Generated: 2025-08-03T13:21:43Z

SELECT appointments.appointment_id, appointments.doctor_id, appointments.start_ts
FROM `project.dataset.appointments` AS appointments
CROSS JOIN `project.dataset.doctors` AS doctors