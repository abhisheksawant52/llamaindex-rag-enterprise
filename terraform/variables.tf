variable "region" {
  description = "AWS region to deploy resources into."
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment name (dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used for tagging and resource naming."
  type        = string
  default     = "llamaindex-rag-enterprise"
}

variable "container_image" {
  description = "Container image reference for the RAG service."
  type        = string
  default     = "llamaindex-rag-enterprise:latest"
}

variable "index_storage_bucket" {
  description = "Name prefix for the S3 bucket used to persist the vector index."
  type        = string
  default     = "llamaindex-rag-index"
}

variable "log_retention_days" {
  description = "Retention period for CloudWatch application logs."
  type        = number
  default     = 30
}

variable "vector_store_instance_type" {
  description = "OpenSearch instance type backing the vector store module."
  type        = string
  default     = "t3.small.search"
}

variable "vector_store_instance_count" {
  description = "Number of data nodes in the vector store cluster."
  type        = number
  default     = 1
}
