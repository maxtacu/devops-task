locals {
  name = "hello-birthday-api"
  db_name = "helloBirthday"
  username = "helloBirthdayUser"
}

module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = local.name

  engine               = "postgres"
  engine_version       = "14"
  family               = "postgres14" # DB parameter group
  major_engine_version = "14"         # DB option group
  instance_class       = "db.t3.micro"
  allocated_storage    = 5
  storage_encrypted    = false

  db_name  = local.db_name
  username = local.username
  port     = 5432

  multi_az               = false
  db_subnet_group_name   = aws_db_subnet_group.default.id
  vpc_security_group_ids = [aws_security_group.rds.id]

  deletion_protection = false

}
