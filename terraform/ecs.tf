locals {
  service_name = "hello-birthday-api"
  app_count = 2
  docker_image = "maxtacu/hello-birthday-api:latest"
  memory_limit = 1024
  cpu_limit = 256
}

resource "aws_ecs_cluster" "hello_birthday" {
  name = local.service_name
}

resource "aws_ecs_service" "hello_birthday" {
  name            = local.service_name
  cluster         = aws_ecs_cluster.hello_birthday.id
  task_definition = aws_ecs_task_definition.hello_birthday.arn
  desired_count   = local.app_count
  launch_type     = "FARGATE"
  
  deployment_minimum_healthy_percent = 50

  network_configuration {
    security_groups = [aws_security_group.hello_birthday_task.id]
    subnets         = aws_subnet.private.*.id
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.hello_birthday.id
    container_name   = local.service_name
    container_port   = 80
  }

  depends_on = [aws_lb_listener.hello_birthday]
}

resource "aws_ecs_task_definition" "hello_birthday" {
  family                   = "service"
  requires_compatibilities = ["FARGATE"]
  memory                   = local.memory_limit
  cpu                      = local.cpu_limit
  execution_role_arn       = aws_iam_role.ecs_task_role.arn
  container_definitions    = jsonencode([{
    name            = "${local.service_name}"
    image           = "${local.docker_image}"
    portMappings    = [
      {
        containerPort = 80
        hostPort      = 80
      }
    ]
    essential   = true
    environment = [
        {"name": "DATABASE_HOST", "value": "${module.db.db_instance_endpoint}"},
        {"name": "DATABASE_USER", "value": "${module.db.db_instance_username}"},
        {"name": "DATABASE_NAME", "value": "${module.db.db_instance_name}"},
        {"name": "DATABASE_PASS", "value": "${module.db.db_instance_password}"}
    ]
    
    logConfiguration = {
        logDriver = "awslogs"
        options = {
            awslogs-group = "${local.service_name}"
            awslogs-region = "eu-west-1"
            awslogs-stream-prefix = "ecs"
            awslogs-create-group = "true"
        }
    }
  }])
  network_mode = "awsvpc"

  depends_on = [module.db]
  
}

# Security group for ECS service
resource "aws_security_group" "ecs_service" {
  name_prefix = "api-ecs-service"
  vpc_id      = aws_vpc.default.id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}