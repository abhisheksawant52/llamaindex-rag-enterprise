locals {
  name_prefix = "${var.project_name}-${var.environment}"
}

# Random suffix to keep the S3 bucket name globally unique.
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Container registry for the RAG service image.
resource "aws_ecr_repository" "app" {
  name                 = local.name_prefix
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# S3 bucket used to persist the LlamaIndex vector index.
resource "aws_s3_bucket" "index_storage" {
  bucket = "${var.index_storage_bucket}-${var.environment}-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket_versioning" "index_storage" {
  bucket = aws_s3_bucket.index_storage.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "index_storage" {
  bucket = aws_s3_bucket.index_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "index_storage" {
  bucket = aws_s3_bucket.index_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Centralised application logs.
resource "aws_cloudwatch_log_group" "app" {
  name              = "/${var.project_name}/${var.environment}"
  retention_in_days = var.log_retention_days
}

# Managed vector store backing the RAG index.
module "vector_store" {
  source = "./modules/vector-store"

  name_prefix    = local.name_prefix
  instance_type  = var.vector_store_instance_type
  instance_count = var.vector_store_instance_count
}
