# Local backend for development/learning purposes
# For production, consider using remote state (S3, Azure Blob, etc.)
terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
