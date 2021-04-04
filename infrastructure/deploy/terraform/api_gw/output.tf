output "api_execution_arn" {
  value = aws_api_gateway_rest_api.api.execution_arn
}

output "api_url" {
  value = aws_api_gateway_deployment.api_deployment.invoke_url
}