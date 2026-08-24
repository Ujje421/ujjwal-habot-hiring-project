# Name: Ujjwal [Last Name]
# Contact: [Email / LinkedIn / GitHub]

variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The default region for resources"
  type        = string
  default     = "asia-south1"
}

variable "bucket_name" {
  description = "The name of the D0 Raw Landing GCS bucket"
  type        = string
}

variable "bq_dataset_id" {
  description = "The ID of the D1 Staged/Enforced BigQuery dataset"
  type        = string
  default     = "d1_staged_enforced"
}

variable "kms_key_id" {
  description = "The full resource name of the KMS key used for CMEK encryption"
  type        = string
}

variable "pipeline_sa_email" {
  description = "The email address of the pipeline service account"
  type        = string
}
