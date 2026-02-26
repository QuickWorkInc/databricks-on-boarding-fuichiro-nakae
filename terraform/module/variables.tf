variable "env" {
  description = "Environment name (dev or stg)"
  type        = string

  validation {
    condition     = contains(["dev", "stg"], var.env)
    error_message = "env must be dev or stg. PRD is NOT allowed."
  }
}

variable "git_source_url" {
  description = "Git repository URL"
  type        = string
  default     = "https://github.com/QuickWorkInc/databricks-on-boarding-fuichiro-nakae.git"
}

variable "git_source_branch" {
  description = "Git branch name"
  type        = string
  default     = "main"
}

variable "notification_destination_id" {
  description = "Slack notification destination ID"
  type        = string
  default     = ""
}

variable "service_principal_name" {
  description = "Service principal name for job execution"
  type        = string
  default     = "e22e080f-69c6-4126-a961-b917cb8db97a"
}
