locals {
  lambda_filename = "./lambda/lambda_function.py"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = local.lambda_filename
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "this" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = var.function_name
  role             = aws_iam_role.lambda_exec.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}

resource "aws_iam_role" "lambda_exec" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  inline_policy {
    name = "lambda-dynamodb-policy"

    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Action   = ["dynamodb:UpdateItem", "dynamodb:GetItem"],
          Effect   = "Allow",
          Resource = "*",
        }
      ],
    })
  }
}

resource "aws_iam_role_policy_attachment" "lambda_exec" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_exec.name
}
