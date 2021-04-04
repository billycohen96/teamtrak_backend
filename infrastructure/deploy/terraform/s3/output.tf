output "s3_bucket" {
  value = aws_s3_bucket.s3_bucket.bucket
}

output "s3_key" {
  value = aws_s3_bucket_object.s3_bucket_object.key
}