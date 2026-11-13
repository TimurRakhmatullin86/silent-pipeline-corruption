-- Generator: gpt-5-2025-08-07
-- Task: bq_041
-- Generated: 2025-10-23T10:31:02Z

SELECT
  daily_revenue.rev_date,
  daily_revenue.business_unit_id,
  daily_revenue.amount,
  SUM(daily_revenue.amount) AS total_amount
FROM `project.dataset.daily_revenue` AS daily_revenue
JOIN `project.dataset.business_units` AS business_units
  ON daily_revenue.business_unit_id = business_units.business_unit_id
WHERE daily_revenue.rev_date >= '2025-01-01'
  AND daily_revenue.rev_date < '2025-07-01'
GROUP BY 1, 2, 3
ORDER BY 1