module "job" {
  source = "../../module"

  env                         = var.env
  notification_destination_id = var.notification_destination_id
  git_source_branch           = var.git_source_branch
}

output "job_id" {
  description = "Databricks Job ID"
  value       = module.job.job_id
}

output "job_name" {
  description = "Databricks Job Name"
  value       = module.job.job_name
}

output "job_url" {
  description = "Databricks Job URL"
  value       = module.job.job_url
}
