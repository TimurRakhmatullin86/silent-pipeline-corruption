-- Generator: deepseek-chat-v3-0324
-- Task: bq_019
-- Generated: 2025-09-17T15:51:35Z

SELECT
  employees.employee_id,
  employees.full_name,
  employees.manager_id
FROM `project.dataset.employees` AS employees
JOIN `project.dataset.departments` AS departments
  ON employees.department_id = departments.department_id
WHERE employees.termination_date >= '2025-01-01'
  AND employees.termination_date < '2025-07-01'