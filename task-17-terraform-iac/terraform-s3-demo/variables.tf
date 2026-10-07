variable "aws_region" {
  description = "Region the bucket is created in"
  type        = string
  default     = "ap-south-1"
}

variable "bucket_name" {
  description = "Globally unique name for the S3 bucket"
  type        = string
}

variable "environment" {
  description = "Environment tag, used on every resource"
  type        = string
  default     = "dev"
}

variable "enable_versioning" {
  description = "Keep old copies of objects when they are overwritten"
  type        = bool
  default     = true
}
