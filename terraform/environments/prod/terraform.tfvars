region                      = "us-east-1"
environment                 = "prod"
project_name                = "llamaindex-rag-enterprise"
container_image             = "llamaindex-rag-enterprise:latest"
index_storage_bucket        = "llamaindex-rag-index"
log_retention_days          = 90
vector_store_instance_type  = "r6g.large.search"
vector_store_instance_count = 3
