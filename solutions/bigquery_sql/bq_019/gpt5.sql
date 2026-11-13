-- Generator: gpt-5-2025-08-07
-- Task: bq_019
-- Generated: 2025-10-21T08:04:42Z

SELECT
  employees.employee_id,
  employees.full_name,
  employees.manager_id
FROM `project.dataset.employees` AS employees
JOIN `project.dataset.departments` AS departments
  ON employees.department_id = departments.department_id
WHERE employees.termination_date >= '2025-01-01'
  AND employees.termination_date < '2025-07-01'
ORDER BY 1