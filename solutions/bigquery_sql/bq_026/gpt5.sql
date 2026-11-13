-- Generator: gpt-5-2025-08-07
-- Task: bq_026
-- Generated: 2025-08-07T10:10:48Z

SELECT
  api_requests.status,
  api_requests.request_id,
  api_requests.endpoint_id,
  api_requests.request_ts
FROM `project.dataset.api_requests` AS api_requests
JOIN `project.dataset.endpoints` AS endpoints
  ON api_requests.endpoint_id = endpoints.endpoint_id
ORDER BY 1