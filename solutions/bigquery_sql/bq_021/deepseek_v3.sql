-- Generator: deepseek-chat-v3-0324
-- Task: bq_021
-- Generated: 2025-10-16T19:05:19Z

SELECT
  employees.employee_id,
  employees.department_id,
  employees.salary
FROM `project.dataset.employees` AS employees
CROSS JOIN `project.dataset.departments` AS departments
WHERE employees.termination_date >= '2025-01-01'
  AND employees.termination_date < '2025-07-01'