// PROJECT endpoint
resource "aws_api_gateway_resource" "project_resource" {
  path_part   = "project"
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "project_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.project_resource.id
}

resource "aws_api_gateway_method" "project_get_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.project_resource.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_method" "project_post_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.project_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "project_post_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_resource.id
  http_method             = aws_api_gateway_method.project_post_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

resource "aws_api_gateway_integration" "project_get_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_resource.id
  http_method             = aws_api_gateway_method.project_get_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// PROJECT/ADD_USER endpoint
resource "aws_api_gateway_resource" "project_add_user_resource" {
  path_part   = "add_user"
  parent_id   = aws_api_gateway_resource.project_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "project_add_user_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.project_add_user_resource.id
}

resource "aws_api_gateway_method" "project_add_user_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.project_add_user_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "project_add_user_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_add_user_resource.id
  http_method             = aws_api_gateway_method.project_add_user_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// PROJECT/REMOVE_USER endpoint
resource "aws_api_gateway_resource" "project_remove_user_resource" {
  path_part   = "remove_user"
  parent_id   = aws_api_gateway_resource.project_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "project_remove_user_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.project_remove_user_resource.id
}

resource "aws_api_gateway_method" "project_remove_user_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.project_remove_user_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "project_remove_user_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_remove_user_resource.id
  http_method             = aws_api_gateway_method.project_remove_user_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// PROJECT/ADD_TASK endpoint
resource "aws_api_gateway_resource" "project_add_task_resource" {
  path_part   = "add_task"
  parent_id   = aws_api_gateway_resource.project_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "project_add_task_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.project_add_task_resource.id
}

resource "aws_api_gateway_method" "project_add_task_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.project_add_task_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "project_add_task_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_add_task_resource.id
  http_method             = aws_api_gateway_method.project_add_task_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

// PROJECT/REMOVE_TASK endpoint
resource "aws_api_gateway_resource" "project_remove_task_resource" {
  path_part   = "remove_task"
  parent_id   = aws_api_gateway_resource.project_resource.id
  rest_api_id = aws_api_gateway_rest_api.api.id
}

module "project_remove_task_resource_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.1"

  api_id          = aws_api_gateway_rest_api.api.id
  api_resource_id = aws_api_gateway_resource.project_remove_task_resource.id
}

resource "aws_api_gateway_method" "project_remove_task_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.project_remove_task_resource.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.auth.id
}

resource "aws_api_gateway_integration" "project_remove_task_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.project_remove_task_resource.id
  http_method             = aws_api_gateway_method.project_remove_task_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}
