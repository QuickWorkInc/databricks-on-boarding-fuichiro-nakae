variable "env" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "notification_destination_id" {
  description = "Slack notification destination ID"
  type        = string
  default     = "8a2a3ad7-9656-4d3e-844d-575330539e2f"
}

variable "git_source_branch" {
  description = "Git branch name"
  type        = string
  default     = "main"
}
