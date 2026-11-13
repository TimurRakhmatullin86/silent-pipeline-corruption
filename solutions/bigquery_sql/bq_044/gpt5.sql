-- Generator: gpt-5-2025-08-07
-- Task: bq_044
-- Generated: 2025-09-23T17:47:46Z

SELECT
  funnel_steps.status,
  funnel_steps.step_order,
  funnel_steps.step_name
FROM `project.dataset.funnel_steps` AS funnel_steps
ORDER BY 1