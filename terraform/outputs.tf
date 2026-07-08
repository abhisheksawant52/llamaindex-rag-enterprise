output "ecr_repository_url" {
  description = "URL of the ECR repository for the service image."
  value       = aws_ecr_repository.app.repository_url
}

output "index_storage_bucket" {
  description = "Name of the S3 bucket used for index persistence."
  value       = aws_s3_bucket.index_storage.bucket
}

output "log_group_name" {
  description = "CloudWatch log group for application logs."
  value       = aws_cloudwatch_log_group.app.name
}

output "vector_store_endpoint" {
  description = "Endpoint of the managed vector store."
  value       = module.vector_store.endpoint
}
