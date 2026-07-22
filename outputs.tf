output "authorized_bucket_arn" {
  value       = aws_s3_bucket.authorized_bucket.arn
  description = "ARN of the compliant S3 bucket."
}

output "unauthorized_bucket_arn" {
  value       = aws_s3_bucket.unauthorized_bucket.arn
  description = "ARN of the non-compliant S3 bucket flagged for cleanup."
}
