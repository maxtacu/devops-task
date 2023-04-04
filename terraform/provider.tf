terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
#   access_key = ""
#   secret_key = ""

  default_tags {
    tags = {
      devopstask = "revolut"
    }
  }
}