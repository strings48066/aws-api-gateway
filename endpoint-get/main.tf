provider "aws" {
  region = "us-east-1" # Replace with your desired AWS region
}

data "aws_caller_identity" "current" {}

module "lambda_dynamodb_dump" {
  source         = "./lambda"
  account_number = data.aws_caller_identity.current.account_id
  function_name  = var.function_name # Replace with your desired Lambda function name
}

resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_dynamodb_dump.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = var.execution_arn
}

resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id             = var.id
  integration_type   = "AWS_PROXY"
  integration_uri    = module.lambda_dynamodb_dump.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = var.id
  route_key = "GET /${var.function_name}"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}