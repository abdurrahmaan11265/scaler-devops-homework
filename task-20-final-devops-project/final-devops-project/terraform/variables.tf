variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "project" {
  description = "Name prefix for every resource"
  type        = string
  default     = "library"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.20.1.0/24"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "allowed_ssh_cidr" {
  description = "Who may SSH to the web server"
  type        = string
  default     = "0.0.0.0/0"
}

variable "bucket_name" {
  type = string
}
