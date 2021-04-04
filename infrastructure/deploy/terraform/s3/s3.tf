data "archive_file" "source" {
  type        = "zip"
  source_dir  = var.artifact_path
  output_path = "${var.artifact_path}.zip"
}

// S3_Bucket to contain python code. Lambda will then pull the code from the S3 bucket to create the function.
resource "aws_s3_bucket" "s3_bucket" {
  bucket = "${var.component_name}-${var.env}-s3"
  acl    = "private"
}

// Create S3_Bucket object from code artifact.
resource "aws_s3_bucket_object" "s3_bucket_object" {
  bucket = aws_s3_bucket.s3_bucket.id
  key    = "${var.component_name}-${var.version_number}-${var.env}-key"
  source = data.archive_file.source.output_path
  etag = filemd5(data.archive_file.source.output_path)
  server_side_encryption = "AES256"

  tags = {
    Environment = var.env
  }
}