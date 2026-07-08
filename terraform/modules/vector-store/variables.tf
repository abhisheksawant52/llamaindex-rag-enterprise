variable "name_prefix" {
  description = "Prefix used to name vector-store resources."
  type        = string
}

variable "instance_type" {
  description = "OpenSearch instance type for data nodes."
  type        = string
  default     = "t3.small.search"
}

variable "instance_count" {
  description = "Number of data nodes in the cluster."
  type        = number
  default     = 1
}

variable "engine_version" {
  description = "OpenSearch engine version."
  type        = string
  default     = "OpenSearch_2.11"
}

variable "volume_size" {
  description = "EBS volume size (GiB) per data node."
  type        = number
  default     = 20
}
