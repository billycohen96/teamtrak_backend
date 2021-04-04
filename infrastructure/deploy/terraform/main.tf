terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
  access_key = var.access_key
  secret_key = var.secret_key
}

module "dynamodb" {
  source = "./dynamodb"
  env = var.env
}

module "api_gw" {
  source = "./api_gw"
  component_name = var.component_name
  env = var.env
  version_number = var.version_number
  lambda_invoke_arn = module.lambda.lambda_invoke_arn
  lambda_name = module.lambda.lambda_name
}

module "lambda" {
  source = "./lambda"
  component_name = var.component_name
  env = var.env
  version_number = var.version_number
  s3_bucket = module.s3.s3_bucket
  s3_key = module.s3.s3_key
  comments_dynamodb_tn = module.dynamodb.comments_table_name
  projects_dynamodb_tn = module.dynamodb.projects_table_name
  tasks_dynamodb_tn = module.dynamodb.tasks_table_name
  users_dynamodb_tn = module.dynamodb.users_table_name
  api_execution_arn = module.api_gw.api_execution_arn
}

module "s3" {
  source = "./s3"
  component_name = var.component_name
  env = var.env
  artifact_path = var.artifact_path
  version_number = var.version_number
}

