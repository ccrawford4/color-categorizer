provider "aws" {
  region = var.region
}

variable "region" {
  description = "The AWS region"
  type        = string
  default     = "us-west-1" # Default region, can be overridden
}

# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect    = "Allow"
      },
    ]
  })
}

# Attach Basic Execution Policy to IAM Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "color_categorizer" {
  function_name     = "colorCategorizerFunction"
  filename          = "lambda_function.zip" # Path to your zip package
  source_code_hash  = filebase64sha256("lambda_function.zip")
  role              = aws_iam_role.lambda_execution_role.arn
  handler           = "lambda_function.handler"
  runtime           = "python3.8"
  memory_size       = 128
  timeout           = 10
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "color_api" {
  name        = "ColorCategorizerAPI"
  description = "API for color categorizer Lambda"
}

# API Gateway Resource for Endpoint
resource "aws_api_gateway_resource" "color_resource" {
  rest_api_id = aws_api_gateway_rest_api.color_api.id
  parent_id   = aws_api_gateway_rest_api.color_api.root_resource_id
  path_part   = "{hex_color}" # Dynamic path for color input
}

# GET Method for the API Resource
resource "aws_api_gateway_method" "color_method" {
  rest_api_id   = aws_api_gateway_rest_api.color_api.id
  resource_id   = aws_api_gateway_resource.color_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# API Gateway Integration with Lambda
resource "aws_api_gateway_integration" "color_integration" {
  rest_api_id             = aws_api_gateway_rest_api.color_api.id
  resource_id             = aws_api_gateway_resource.color_resource.id
  http_method             = aws_api_gateway_method.color_method.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${aws_lambda_function.color_categorizer.arn}/invocations"
}

# Allow API Gateway to Invoke Lambda
resource "aws_lambda_permission" "allow_api_gateway" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.color_categorizer.function_name
  principal     = "apigateway.amazonaws.com"
  statement_id  = "AllowAPIGatewayInvoke"
}

# Deploy the API Gateway
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.color_api.id
  triggers = {
    redeployment = timestamp() # Forces new deployment when needed
  }

  depends_on = [aws_api_gateway_integration.color_integration]
}

# Create a Stage for the Deployment
resource "aws_api_gateway_stage" "prod_stage" {
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.color_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
  description   = "Production stage for ColorCategorizerAPI"
}

# Output the API Gateway URL
output "api_gateway_url" {
  value = "https://${aws_api_gateway_rest_api.color_api.id}.execute-api.${var.region}.amazonaws.com/prod"
  description = "The URL for the deployed API Gateway"
}