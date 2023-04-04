resource "aws_lb" "hello_birthday" {
  name            = local.service_name
  subnets         = aws_subnet.public.*.id
  security_groups = [aws_security_group.lb.id]
}

resource "aws_lb_target_group" "hello_birthday" {
  name        = "birthday-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.default.id
  target_type = "ip"

  health_check {
    path    = "/docs"
    interval = 120
  }
}

resource "aws_lb_listener" "hello_birthday" {
  load_balancer_arn = aws_lb.hello_birthday.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.hello_birthday.id
    type             = "forward"
  }
}

output "load_balancer_ip" {
  value = aws_lb.hello_birthday.dns_name
}