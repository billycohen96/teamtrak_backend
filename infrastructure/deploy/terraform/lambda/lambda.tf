// LAMBDA IAM ROLE:
resource aws_iam_role_policy lambda_function_iam_role_policy {
  role = aws_iam_role.lambda_function_iam_role.id
  policy = <<-POLICY
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "dynamodb:BatchGetItem",
          "dynamodb:BatchWriteItem",
          "dynamodb:ConditionCheckItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:UpdateItem",
          "dynamodb:GetRecords"
        ],
        "Resource": "*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "kms:Decrypt"
        ],
        "Resource": "*"
      }
    ]
  }
  POLICY
  depends_on = [aws_iam_role.lambda_function_iam_role]
}

// IAM role assigned to the API function
resource aws_iam_role "lambda_function_iam_role" {
  name = "${var.component_name}-${var.env}-iam-role"
  description = "IAM role for API lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

// LAMBDA FUNCTION
resource "aws_lambda_function" "lambda_function" {
  function_name = "${var.component_name}-${var.version_number}-${var.env}-lambda"
  handler = "kio_prog_api.lambda_function.handler"
  role = aws_iam_role.lambda_function_iam_role.arn
  runtime = "python3.7"
  description = "Lambda function for handling API requests"
  s3_bucket = var.s3_bucket
  s3_key = var.s3_key

  environment {
    variables = {
      PROJECT_TN = var.projects_dynamodb_tn
      TASK_TN = var.tasks_dynamodb_tn
      USER_TN = var.users_dynamodb_tn
      COMMENT_TN = var.comments_dynamodb_tn
      TEMPLATE_TN = ""
    }
  }

  tags = {
    Environment = var.env
  }

  depends_on = [
    var.s3_bucket,
    var.s3_key,
    var.projects_dynamodb_tn,
    var.tasks_dynamodb_tn,
    var.users_dynamodb_tn,
    var.comments_dynamodb_tn,
    aws_iam_role.lambda_function_iam_role,
    aws_iam_role_policy.lambda_function_iam_role_policy
  ]
}