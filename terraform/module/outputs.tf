output "job_id" {
  description = "Databricks Job ID"
  value       = databricks_job.main.id
}

output "job_name" {
  description = "Databricks Job Name"
  value       = databricks_job.main.name
}

output "job_url" {
  description = "Databricks Job URL"
  value       = databricks_job.main.url
}
