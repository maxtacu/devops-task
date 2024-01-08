terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
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