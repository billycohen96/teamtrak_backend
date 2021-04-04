// APIGW Root
# API Gateway

data "aws_cognito_user_pools" "pool" {
  name = "kanbanio"
}

resource "aws_api_gateway_rest_api" "api" {
  name = "${var.component_name}-${var.version_number}-${var.env}-apigw"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  depends_on = [
    aws_api_gateway_integration.comment_post_integration,
    aws_api_gateway_integration.comment_get_integration,
    aws_api_gateway_integration.project_post_integration,
    aws_api_gateway_integration.project_get_integration,
    aws_api_gateway_integration.user_get_integration,
    aws_api_gateway_integration.user_post_integration,
    aws_api_gateway_integration.task_post_integration,
    aws_api_gateway_integration.task_get_integration,
    aws_api_gateway_integration.comment_downvote_integration,
    aws_api_gateway_integration.comment_upvote_integration,
    aws_api_gateway_integration.task_add_comment_integration,
    aws_api_gateway_integration.task_remove_comment_integration,
    aws_api_gateway_integration.task_add_user_integration,
    aws_api_gateway_integration.task_remove_user_integration,
    aws_api_gateway_integration.project_add_task_integration,
    aws_api_gateway_integration.project_add_user_integration,
    aws_api_gateway_integration.project_remove_task_integration,
    aws_api_gateway_integration.project_remove_user_integration,
    aws_api_gateway_integration.user_add_project_integration,
    aws_api_gateway_integration.user_remove_project_integration
  ]
}

resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = var.env
}

resource "aws_api_gateway_authorizer" "auth" {
  name                   = "Cognito"
  rest_api_id            = aws_api_gateway_rest_api.api.id
  type = "COGNITO_USER_POOLS"
  provider_arns = data.aws_cognito_user_pools.pool.arns
}

resource "aws_lambda_permission" "lambda_apigw_permission" {
  statement_id  = "AllowExecutionFromAPIGW"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_name
  principal     = "apigateway.amazonaws.com"
}