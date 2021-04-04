// TASK endpoint
resource "aws_api_gateway_resource" "task_resource" {
  path_part   = "task"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "cors_task_resource" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.task_resource.id
}

resource "aws_api_gateway_method" "task_post_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.task_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_method" "task_get_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.task_resource.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "task_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.task_resource.id
  http_method             = aws_api_gateway_method.task_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

resource "aws_api_gateway_integration" "task_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.task_resource.id
  http_method             = aws_api_gateway_method.task_get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// TASK/ADD_USER endpoint
resource "aws_api_gateway_resource" "task_add_user_resource" {
  path_part   = "add_user"
  parent_id   = aws_api_gateway_resource.task_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "task_add_user_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.task_add_user_resource.id
}

resource "aws_api_gateway_method" "task_add_user_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.task_add_user_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "task_add_user_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.task_add_user_resource.id
  http_method             = aws_api_gateway_method.task_add_user_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// TASK/REMOVE_USER endpoint
resource "aws_api_gateway_resource" "task_remove_user_resource" {
  path_part   = "remove_user"
  parent_id   = aws_api_gateway_resource.task_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "task_remove_user_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.task_remove_user_resource.id
}

resource "aws_api_gateway_method" "task_remove_user_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.task_remove_user_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "task_remove_user_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.task_remove_user_resource.id
  http_method             = aws_api_gateway_method.task_remove_user_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// TASK/ADD_COMMENT endpoint
resource "aws_api_gateway_resource" "task_add_comment_resource" {
  path_part   = "add_comment"
  parent_id   = aws_api_gateway_resource.task_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "task_add_comment_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.task_add_comment_resource.id
}

resource "aws_api_gateway_method" "task_add_comment_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.task_add_comment_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "task_add_comment_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.task_add_comment_resource.id
  http_method             = aws_api_gateway_method.task_add_comment_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// TASK/REMOVE_COMMENT endpoint
resource "aws_api_gateway_resource" "task_remove_comment_resource" {
  path_part   = "remove_comment"
  parent_id   = aws_api_gateway_resource.task_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "task_remove_comment_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.task_remove_comment_resource.id
}

resource "aws_api_gateway_method" "task_remove_comment_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.task_remove_comment_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "task_remove_comment_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.task_remove_comment_resource.id
  http_method             = aws_api_gateway_method.task_remove_comment_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}