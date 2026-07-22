# Authorized / Compliant S3 Bucket (Has the required Project tag)
resource "aws_s3_bucket" "authorized_bucket" {
  bucket        = var.authorized_bucket_name
  force_destroy = true

  tags = {
    Name        = var.authorized_bucket_name
    Environment = var.environment
    Project     = "Sentinel-Cloud" # Mandatory tag for FinOps compliance
  }
}

# Untagged / Non-Compliant S3 Bucket (Simulates Shadow IT waste)
resource "aws_s3_bucket" "unauthorized_bucket" {
  bucket        = "sentinel-untracked-waste-bucket"
  force_destroy = true

  # Intentionally missing the "Project" tag to trigger Sentinel cleanup
  tags = {
    Environment = var.environment
  }
}
