output "users_table_arn" {
  value = aws_dynamodb_table.users_table.arn
}

output "users_table_name" {
  value = aws_dynamodb_table.users_table.name
}

output "tasks_table_arn" {
  value = aws_dynamodb_table.tasks_table.arn
}

output "tasks_table_name" {
  value = aws_dynamodb_table.tasks_table.name
}

output "projects_table_arn" {
  value = aws_dynamodb_table.projects_table.arn
}

output "projects_table_name" {
  value = aws_dynamodb_table.projects_table.name
}

output "comments_table_arn" {
  value = aws_dynamodb_table.comments_table.arn
}

output "comments_table_name" {
  value = aws_dynamodb_table.comments_table.name
}