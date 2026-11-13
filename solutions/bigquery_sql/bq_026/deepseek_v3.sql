-- Generator: deepseek-chat-v3-0324
-- Task: bq_026
-- Generated: 2025-10-20T09:57:40Z

SELECT
  api_requests.request_id,
  api_requests.endpoint_id,
  api_requests.request_ts
FROM `project.dataset.api_requests` AS api_requests
JOIN `project.dataset.endpoints` AS endpoints
  ON api_requests.endpoint_id = endpoints.endpoint_id