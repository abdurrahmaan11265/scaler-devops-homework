resource "aws_s3_bucket" "demo" {
  bucket = var.bucket_name

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Separate resources configure the bucket. They depend on the bucket
# implicitly because they reference aws_s3_bucket.demo.id.
resource "aws_s3_bucket_versioning" "demo" {
  bucket = aws_s3_bucket.demo.id
  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_public_access_block" "demo" {
  bucket                  = aws_s3_bucket.demo.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# One object uploaded so terraform show and the console have something to list.
resource "aws_s3_object" "readme" {
  bucket  = aws_s3_bucket.demo.id
  key     = "hello.txt"
  content = "created by terraform for the session 18 homework\n"
}
