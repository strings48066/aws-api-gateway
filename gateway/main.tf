provider "aws" {
  region = "us-east-1" # Replace with your desired AWS region
}

data "aws_caller_identity" "current" {}


resource "aws_apigatewayv2_api" "api_gateway" {
  name          = var.gw_name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "api_gateway_stage" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "prod"
  auto_deploy = true
}

resource "aws_apigatewayv2_stage" "api_gateway_stage_nonprod" {
  api_id      = aws_apigatewayv2_api.api_gateway.id
  name        = "develop"
  auto_deploy = true
}