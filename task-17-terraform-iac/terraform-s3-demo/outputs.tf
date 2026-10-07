output "bucket_name" {
  description = "Name of the bucket that was created"
  value       = aws_s3_bucket.demo.id
}

output "bucket_arn" {
  value = aws_s3_bucket.demo.arn
}

output "bucket_region" {
  value = aws_s3_bucket.demo.region
}

output "versioning" {
  value = aws_s3_bucket_versioning.demo.versioning_configuration[0].status
}
