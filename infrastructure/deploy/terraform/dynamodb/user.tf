resource "aws_dynamodb_table" "users_table" {
  name = "users-${var.env}"

  billing_mode   = "PROVISIONED"

  read_capacity  = 20
  write_capacity = 20

  hash_key = "email_address"
  attribute {
    name = "email_address"
    type = "S"
  }
}