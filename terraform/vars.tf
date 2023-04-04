# variable "db_password" {
#   description = "RDS root user password"
#   type        = string
#   sensitive   = true
# }

variable "aws_region" {
    type        = string
    description = "AWS region"
    default     = "eu-west-1"
}