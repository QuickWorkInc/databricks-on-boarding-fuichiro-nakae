terraform {
  required_version = ">= 1.0.0"

  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">= 1.0.0"
    }
  }
}

provider "databricks" {
  # Authentication is configured via environment variables or CLI config:
  # - DATABRICKS_HOST
  # - DATABRICKS_TOKEN
  # Or use databricks CLI: databricks configure
}
