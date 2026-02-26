variable "env" {
  description = "Environment name"
  type        = string
  default     = "stg"
}

variable "notification_destination_id" {
  description = "Slack notification destination ID"
  type        = string
  default     = ""
}

variable "git_source_branch" {
  description = "Git branch name"
  type        = string
  default     = "main"
}
